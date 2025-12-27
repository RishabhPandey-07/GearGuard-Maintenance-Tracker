import { useState, useEffect } from "react";
import {
  Package,
  Wrench,
  Users,
  AlertTriangle,
  TrendingUp,
  Clock,
} from "lucide-react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { dashboardAPI } from "../api/services";

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [requestsByTeam, setRequestsByTeam] = useState([]);
  const [equipmentByCategory, setEquipmentByCategory] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [statsRes, requestsRes, equipmentRes, activityRes] =
        await Promise.all([
          dashboardAPI.getStats(),
          dashboardAPI.getRequestsByTeam(),
          dashboardAPI.getEquipmentByCategory(),
          dashboardAPI.getRecentActivity(),
        ]);

      setStats(statsRes.data);
      setRequestsByTeam(requestsRes.data);
      setEquipmentByCategory(equipmentRes.data);
      setRecentActivity(activityRes.data);
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ["#9333ea", "#a855f7", "#c084fc", "#d8b4fe", "#e9d5ff"];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-700"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Overview of your maintenance operations
          </p>
        </div>
        <button onClick={fetchDashboardData} className="btn-secondary">
          <Clock className="w-4 h-4 inline mr-2" />
          Refresh
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">
                Total Equipment
              </p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats?.total_equipment || 0}
              </p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Package className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">
                Active Requests
              </p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats?.active_requests || 0}
              </p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <Wrench className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Overdue</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats?.overdue_requests || 0}
              </p>
            </div>
            <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <AlertTriangle className="w-6 h-6 text-red-600" />
            </div>
          </div>
        </div>

        <div className="glass-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Teams</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats?.total_teams || 0}
              </p>
            </div>
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <Users className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Requests by Team */}
        <div className="glass-card p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Requests by Team
          </h2>
          {requestsByTeam.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={requestsByTeam}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="team" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#9333ea" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center py-12">No data available</p>
          )}
        </div>

        {/* Equipment by Category */}
        <div className="glass-card p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Equipment by Category
          </h2>
          {equipmentByCategory.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={equipmentByCategory}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ category, count }) =>
                    `${category}: ${count}`
                  }
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count">
                  {equipmentByCategory.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center py-12">
              No equipment data available
            </p>
          )}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="glass-card p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Recent Activity
        </h2>
        {recentActivity.length > 0 ? (
          <div className="space-y-4">
            {recentActivity.map((activity) => (
              <div
                key={activity.id}
                className="flex items-start gap-4 p-4 bg-gray-50 rounded-lg">
                <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <TrendingUp className="w-5 h-5 text-purple-600" />
                </div>
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{activity.action}</p>
                  <p className="text-sm text-gray-600 mt-1">
                    {activity.description}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {new Date(activity.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">No recent activity</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
