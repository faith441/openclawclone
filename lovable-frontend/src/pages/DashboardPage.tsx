import { useQuery } from '@tanstack/react-query';
import { executionsAPI } from '../lib/api';
import { Activity, TrendingUp, DollarSign, Clock } from 'lucide-react';

export default function DashboardPage() {
  const { data: stats } = useQuery({
    queryKey: ['execution-stats'],
    queryFn: () => executionsAPI.getStats('week'),
  });

  const { data: historyData } = useQuery({
    queryKey: ['execution-history'],
    queryFn: () => executionsAPI.getHistory(10, 0),
  });

  const executions = historyData?.data?.executions || [];

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Executions</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.data?.total_executions || 0}
              </p>
            </div>
            <Activity className="w-10 h-10 text-blue-600" />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Success Rate</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.data?.success_rate || 0}%
              </p>
            </div>
            <TrendingUp className="w-10 h-10 text-green-600" />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Cost</p>
              <p className="text-2xl font-bold text-gray-900">
                ${stats?.data?.total_cost?.toFixed(2) || '0.00'}
              </p>
            </div>
            <DollarSign className="w-10 h-10 text-purple-600" />
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Avg. Duration</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.data?.avg_duration?.toFixed(1) || '0'}s
              </p>
            </div>
            <Clock className="w-10 h-10 text-orange-600" />
          </div>
        </div>
      </div>

      {/* Recent Executions */}
      <div className="bg-white rounded-xl shadow-sm">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent Executions</h2>
        </div>
        <div className="divide-y divide-gray-200">
          {executions.length === 0 ? (
            <div className="px-6 py-12 text-center text-gray-500">
              <p>No executions yet. Create your first automation!</p>
            </div>
          ) : (
            executions.map((execution: any) => (
              <div key={execution.id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-gray-900">{execution.agent_id}</p>
                    <p className="text-sm text-gray-600">{execution.created_at}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        execution.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : execution.status === 'failed'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}
                    >
                      {execution.status}
                    </span>
                    {execution.cost && (
                      <span className="text-sm text-gray-600">
                        ${execution.cost.toFixed(4)}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
