/**
 * API routes for managing user AI API keys
 * POST /api/ai-keys - Add or update an AI API key
 * GET /api/ai-keys - List user's configured AI providers
 * DELETE /api/ai-keys/:provider - Remove an API key
 */

import { NextRequest, NextResponse } from 'next/server';
import { encrypt, decrypt, maskApiKey } from '@/lib/encryption';
import { supabaseAdmin, getCurrentUser } from '@/lib/supabase';
import { testApiKey } from '@/lib/cloud-executor';

/**
 * GET /api/ai-keys - List user's AI providers
 */
export async function GET(request: NextRequest) {
  try {
    const user = await getCurrentUser(request.headers.get('authorization') || undefined);
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { data, error } = await supabaseAdmin
      .from('user_ai_keys')
      .select('provider, is_active, last_tested, test_status, created_at')
      .eq('user_id', user.id);

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ providers: data || [] });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

/**
 * POST /api/ai-keys - Add or update an AI API key
 */
export async function POST(request: NextRequest) {
  try {
    const user = await getCurrentUser(request.headers.get('authorization') || undefined);
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { provider, apiKey, testKey } = body;

    if (!provider || !apiKey) {
      return NextResponse.json(
        { error: 'Provider and apiKey are required' },
        { status: 400 }
      );
    }

    // Validate provider
    const validProviders = ['openai', 'anthropic', 'google', 'groq'];
    if (!validProviders.includes(provider)) {
      return NextResponse.json(
        { error: `Invalid provider. Must be one of: ${validProviders.join(', ')}` },
        { status: 400 }
      );
    }

    // Test the API key if requested
    let testStatus = 'not_tested';
    let testError = null;

    if (testKey) {
      const testResult = await testApiKey(provider, apiKey);
      testStatus = testResult.valid ? 'valid' : 'invalid';
      testError = testResult.error;

      if (!testResult.valid) {
        return NextResponse.json(
          {
            error: 'API key validation failed',
            details: testError
          },
          { status: 400 }
        );
      }
    }

    // Encrypt the API key
    const encryptedKey = encrypt(apiKey);

    // Upsert the key
    const { data, error } = await supabaseAdmin
      .from('user_ai_keys')
      .upsert(
        {
          user_id: user.id,
          provider,
          encrypted_key: encryptedKey,
          is_active: true,
          last_tested: testKey ? new Date().toISOString() : null,
          test_status: testStatus,
        },
        {
          onConflict: 'user_id,provider',
        }
      )
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({
      success: true,
      provider: data.provider,
      testStatus: data.test_status,
      message: `${provider} API key ${testKey ? 'validated and ' : ''}saved successfully`,
    });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

/**
 * DELETE /api/ai-keys - Remove an API key
 */
export async function DELETE(request: NextRequest) {
  try {
    const user = await getCurrentUser(request.headers.get('authorization') || undefined);
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const provider = searchParams.get('provider');

    if (!provider) {
      return NextResponse.json(
        { error: 'Provider parameter is required' },
        { status: 400 }
      );
    }

    const { error } = await supabaseAdmin
      .from('user_ai_keys')
      .delete()
      .eq('user_id', user.id)
      .eq('provider', provider);

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({
      success: true,
      message: `${provider} API key removed successfully`,
    });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
