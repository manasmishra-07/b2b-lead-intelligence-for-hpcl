import { useQuery } from '@tanstack/react-query';
import { TrendingUp, Users, Target, AlertCircle } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function Dashboard() {
  // Fetch summary stats
  const { data: stats, isLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/stats/summary`);
      return response.data;
    },
  });

  const kpiCards = [
    {
      title: 'Total Leads',
      value: stats?.total_leads || 0,
      icon: Target,
      color: 'bg-blue-500',
      textColor: 'text-blue-600',
      bgColor: 'bg-blue-50 dark:bg-blue-900/20',
    },
    {
      title: 'Active Leads',
      value: stats?.active_leads || 0,
      icon: TrendingUp,
      color: 'bg-green-500',
      textColor: 'text-green-600',
      bgColor: 'bg-green-50 dark:bg-green-900/20',
    },
    {
      title: 'Total Companies',
      value: stats?.total_companies || 0,
      icon: Users,
      color: 'bg-purple-500',
      textColor: 'text-purple-600',
      bgColor: 'bg-purple-50 dark:bg-purple-900/20',
    },
    {
      title: 'Sales Officers',
      value: stats?.total_officers || 0,
      icon: AlertCircle,
      color: 'bg-orange-500',
      textColor: 'text-orange-600',
      bgColor: 'bg-orange-50 dark:bg-orange-900/20',
    },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-hpcl-blue border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-hpcl-blue to-hpcl-darkBlue rounded-lg p-8 text-white">
        <h2 className="text-3xl font-bold mb-2">Welcome to HPCL Lead Intelligence</h2>
        <p className="text-blue-100">
          Monitor and manage B2B leads for Direct Sales & Bulk Fuels division
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpiCards.map((kpi, index) => (
          <div
            key={index}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                  {kpi.title}
                </p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">
                  {kpi.value}
                </p>
              </div>
              <div className={`${kpi.bgColor} p-4 rounded-lg`}>
                <kpi.icon className={`w-8 h-8 ${kpi.textColor}`} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            Recent Activity
          </h3>
          <div className="space-y-4">
            <div className="flex items-start space-x-3 pb-4 border-b border-gray-200 dark:border-gray-700">
              <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  New lead generated
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Reliance Industries - Bitumen requirement
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-3 pb-4 border-b border-gray-200 dark:border-gray-700">
              <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  Lead updated
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Tata Steel - Contacted status
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  New company added
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  JSW Steel registered
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
            System Status
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Backend API
              </span>
              <span className="px-3 py-1 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 rounded-full text-xs font-medium">
                Connected
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Database
              </span>
              <span className="px-3 py-1 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 rounded-full text-xs font-medium">
                Active
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Last Sync
              </span>
              <span className="text-sm text-gray-900 dark:text-white font-medium">
                Just now
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;