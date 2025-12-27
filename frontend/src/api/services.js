import api from "./axios";

// Equipment API
export const equipmentAPI = {
  getAll: () => api.get("/equipment"),
  getById: (id) => api.get(`/equipment/${id}`),
  create: (data) => api.post("/equipment", data),
  update: (id, data) => api.put(`/equipment/${id}`, data),
  delete: (id) => api.delete(`/equipment/${id}`),
  getByTeam: (teamId) => api.get(`/equipment/by-team/${teamId}`),
  getByStatus: (status) => api.get(`/equipment/by-status/${status}`),
};

// Maintenance Requests API
export const requestsAPI = {
  getAll: (params) => api.get("/requests", { params }),
  getById: (id) => api.get(`/requests/${id}`),
  create: (data) => api.post("/requests", data),
  update: (id, data) => api.put(`/requests/${id}`, data),
  delete: (id) => api.delete(`/requests/${id}`),
  getByEquipment: (equipmentId) =>
    api.get(`/requests/by-equipment/${equipmentId}`),
  getByStage: (stage) => api.get(`/requests/by-stage/${stage}`),
  getPreventive: () => api.get("/requests/preventive"),
};

// Teams API
export const teamsAPI = {
  getAll: () => api.get("/teams"),
  getById: (id) => api.get(`/teams/${id}`),
  create: (data) => api.post("/teams", data),
  delete: (id) => api.delete(`/teams/${id}`),

  // Team Members
  getAllMembers: () => api.get("/teams/members"),
  getTeamMembers: (teamId) => api.get(`/teams/${teamId}/members`),
  createMember: (data) => api.post("/teams/members", data),
  updateMember: (id, data) => api.put(`/teams/members/${id}`, data),
  deleteMember: (id) => api.delete(`/teams/members/${id}`),
};

// Dashboard API
export const dashboardAPI = {
  getStats: () => api.get("/dashboard/stats"),
  getRequestsByTeam: () => api.get("/dashboard/requests-by-team"),
  getEquipmentByCategory: () => api.get("/dashboard/equipment-by-category"),
  getRecentActivity: () => api.get("/dashboard/recent-activity"),
};

export default {
  equipment: equipmentAPI,
  requests: requestsAPI,
  teams: teamsAPI,
  dashboard: dashboardAPI,
};
