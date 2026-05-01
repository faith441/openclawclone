'use client';

import { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function Home() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [apiKey, setApiKey] = useState('');
  const [provider, setProvider] = useState('openai');
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState('');
  const [executing, setExecuting] = useState(false);
  const [hasApiKey, setHasApiKey] = useState(false);
  const [message, setMessage] = useState('');

  // Check auth state
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
      if (session?.user) {
        checkApiKeys(session.access_token);
      }
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
      if (session?.user) {
        checkApiKeys(session.access_token);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const checkApiKeys = async (token: string) => {
    try {
      const res = await fetch('/api/ai-keys', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      setHasApiKey(data.providers?.length > 0);
    } catch (e) {
      console.error('Error checking API keys:', e);
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const email = (form.elements.namedItem('email') as HTMLInputElement).value;
    const password = (form.elements.namedItem('password') as HTMLInputElement).value;

    const { error } = await supabase.auth.signUp({ email, password });
    if (error) {
      setMessage(`Error: ${error.message}`);
    } else {
      setMessage('Check your email to confirm your account!');
    }
  };

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const email = (form.elements.namedItem('email') as HTMLInputElement).value;
    const password = (form.elements.namedItem('password') as HTMLInputElement).value;

    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    setHasApiKey(false);
  };

  const saveApiKey = async () => {
    if (!apiKey.trim()) {
      setMessage('Please enter an API key');
      return;
    }

    setMessage('Testing and saving API key...');

    try {
      const session = await supabase.auth.getSession();
      const token = session.data.session?.access_token;

      const res = await fetch('/api/ai-keys', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          provider,
          apiKey,
          testKey: true
        })
      });

      const data = await res.json();

      if (res.ok) {
        setMessage(`✅ ${data.message}`);
        setHasApiKey(true);
        setApiKey('');
      } else {
        setMessage(`❌ ${data.error}: ${data.details || ''}`);
      }
    } catch (e: any) {
      setMessage(`❌ Error: ${e.message}`);
    }
  };

  const runWorkflow = async () => {
    if (!prompt.trim()) {
      setMessage('Please enter a prompt');
      return;
    }

    setExecuting(true);
    setResult('');
    setMessage('Executing...');

    try {
      const session = await supabase.auth.getSession();
      const token = session.data.session?.access_token;

      // For this simple test, we'll call the execute API directly
      // In production, this would use a proper workflow
      const res = await fetch('/api/execute', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          workflowId: 'test-workflow',
          skillId: 'direct-prompt',
          parameters: {
            prompt: prompt
          }
        })
      });

      const data = await res.json();

      if (res.ok && data.success) {
        setResult(data.output);
        setMessage(`✅ Done! Tokens: ${data.tokensUsed} | Cost: $${data.cost?.toFixed(4) || '0.00'}`);
      } else {
        setMessage(`❌ ${data.error}`);
        if (data.logs) {
          setResult(data.logs.join('\n'));
        }
      }
    } catch (e: any) {
      setMessage(`❌ Error: ${e.message}`);
    } finally {
      setExecuting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold mb-2">☁️ Zenthral Cloud Mode</h1>
        <p className="text-gray-400 mb-8">AI automation without installation</p>

        {message && (
          <div className={`p-4 rounded mb-6 ${message.startsWith('✅') ? 'bg-green-900' : message.startsWith('❌') ? 'bg-red-900' : 'bg-blue-900'}`}>
            {message}
          </div>
        )}

        {!user ? (
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Sign In or Sign Up</h2>
            <form onSubmit={handleSignIn} className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Email</label>
                <input
                  name="email"
                  type="email"
                  required
                  className="w-full p-3 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 outline-none"
                  placeholder="you@example.com"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Password</label>
                <input
                  name="password"
                  type="password"
                  required
                  className="w-full p-3 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 outline-none"
                  placeholder="••••••••"
                />
              </div>
              <div className="flex gap-3">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700 py-3 rounded font-semibold"
                >
                  Sign In
                </button>
                <button
                  type="button"
                  onClick={handleSignUp}
                  className="flex-1 bg-gray-600 hover:bg-gray-700 py-3 rounded font-semibold"
                >
                  Sign Up
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-between items-center bg-gray-800 rounded-lg p-4">
              <span>Logged in as: <strong>{user.email}</strong></span>
              <button
                onClick={handleSignOut}
                className="text-red-400 hover:text-red-300"
              >
                Sign Out
              </button>
            </div>

            {/* Step 1: Add API Key */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">
                Step 1: Add AI API Key {hasApiKey && '✅'}
              </h2>
              {hasApiKey ? (
                <p className="text-green-400">API key configured! You can run workflows.</p>
              ) : (
                <div className="space-y-4">
                  <p className="text-gray-400">
                    Get a free API key from <a href="https://platform.openai.com/api-keys" target="_blank" className="text-blue-400 hover:underline">OpenAI</a> or <a href="https://console.anthropic.com" target="_blank" className="text-blue-400 hover:underline">Anthropic</a>
                  </p>
                  <div className="flex gap-3">
                    <select
                      value={provider}
                      onChange={(e) => setProvider(e.target.value)}
                      className="p-3 bg-gray-700 rounded border border-gray-600"
                    >
                      <option value="openai">OpenAI</option>
                      <option value="anthropic">Anthropic</option>
                    </select>
                    <input
                      type="password"
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                      placeholder="sk-..."
                      className="flex-1 p-3 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 outline-none"
                    />
                    <button
                      onClick={saveApiKey}
                      className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded font-semibold"
                    >
                      Save
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Step 2: Run Workflow */}
            <div className="bg-gray-800 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Step 2: Run AI Workflow</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-1">Your Prompt</label>
                  <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Write a professional email to..."
                    className="w-full p-3 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 outline-none h-32"
                  />
                </div>
                <button
                  onClick={runWorkflow}
                  disabled={!hasApiKey || executing}
                  className={`w-full py-3 rounded font-semibold ${
                    hasApiKey && !executing
                      ? 'bg-blue-600 hover:bg-blue-700'
                      : 'bg-gray-600 cursor-not-allowed'
                  }`}
                >
                  {executing ? '⏳ Executing...' : hasApiKey ? '🚀 Run' : '🔑 Add API Key First'}
                </button>
              </div>
            </div>

            {/* Results */}
            {result && (
              <div className="bg-gray-800 rounded-lg p-6">
                <h2 className="text-xl font-semibold mb-4">📄 Result</h2>
                <div className="bg-gray-900 p-4 rounded whitespace-pre-wrap font-mono text-sm">
                  {result}
                </div>
                <div className="mt-4 flex gap-3">
                  <button
                    onClick={() => navigator.clipboard.writeText(result)}
                    className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded"
                  >
                    📋 Copy
                  </button>
                  <button
                    onClick={() => setResult('')}
                    className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded"
                  >
                    🗑️ Clear
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
