/**
 * Cloud execution API endpoint
 * POST /api/execute - Execute a workflow in cloud mode
 */

import { NextRequest, NextResponse } from 'next/server';
import { getCurrentUser } from '@/lib/supabase';
import { executeWorkflow } from '@/lib/cloud-executor';

/**
 * POST /api/execute - Execute a workflow in the cloud
 */
export async function POST(request: NextRequest) {
  try {
    const user = await getCurrentUser(request.headers.get('authorization') || undefined);
    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { workflowId, skillId, parameters } = body;

    if (!workflowId) {
      return NextResponse.json(
        { error: 'workflowId is required' },
        { status: 400 }
      );
    }

    // Execute the workflow
    const result = await executeWorkflow({
      userId: user.id,
      workflowId,
      skillId: skillId || 'unknown',
      parameters: parameters || {},
    });

    if (!result.success) {
      return NextResponse.json(
        {
          success: false,
          error: result.error,
          logs: result.logs,
        },
        { status: 400 }
      );
    }

    return NextResponse.json({
      success: true,
      output: result.output,
      tokensUsed: result.tokensUsed,
      cost: result.cost,
      logs: result.logs,
    });
  } catch (error: any) {
    console.error('Execution error:', error);
    return NextResponse.json(
      {
        success: false,
        error: error.message || 'Execution failed',
        logs: [`Error: ${error.message}`],
      },
      { status: 500 }
    );
  }
}
