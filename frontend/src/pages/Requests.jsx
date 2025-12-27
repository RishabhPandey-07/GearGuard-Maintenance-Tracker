import { useState } from "react";
import { Plus, Edit2, Trash2, Filter, Wrench } from "lucide-react";
import { useApp } from "../context/AppContext";

const Requests = () => {
  const { requests, equipment, addRequest, updateRequest, deleteRequest } =
    useApp();
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [filterStage, setFilterStage] = useState("all");
  const [formData, setFormData] = useState({
    equipment_id: "",
    request_type: "Corrective",
    priority: "Medium",
    stage: "New",
    description: "",
    scheduled_date: "",
    completed_date: "",
  });

  const filteredRequests =
    filterStage === "all"
      ? requests
      : requests.filter((item) => item.stage === filterStage);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await updateRequest(editingItem.id, formData);
      } else {
        await addRequest(formData);
      }
      closeModal();
    } catch (error) {
      console.error("Error saving request:", error);
      alert("Failed to save request");
    }
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setFormData({
      equipment_id: item.equipment_id,
      request_type: item.request_type,
      priority: item.priority,
      stage: item.stage,
      description: item.description,
      scheduled_date: item.scheduled_date || "",
      completed_date: item.completed_date || "",
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this request?")) {
      try {
        await deleteRequest(id);
      } catch (error) {
        console.error("Error deleting request:", error);
        alert("Failed to delete request");
      }
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingItem(null);
    setFormData({
      equipment_id: "",
      request_type: "Corrective",
      priority: "Medium",
      stage: "New",
      description: "",
      scheduled_date: "",
      completed_date: "",
    });
  };

  const getPriorityBadge = (priority) => {
    const badges = {
      Low: "badge-info",
      Medium: "badge-warning",
      High: "badge-danger",
      Critical: "badge-danger",
    };
    return badges[priority] || "badge-default";
  };

  const getStageBadge = (stage) => {
    const badges = {
      New: "badge-info",
      "In Progress": "badge-warning",
      Repaired: "badge-success",
      Scrap: "badge-danger",
    };
    return badges[stage] || "badge-default";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">
            Maintenance Requests
          </h1>
          <p className="text-gray-600 mt-1">
            Track and manage maintenance requests
          </p>
        </div>
        <button onClick={() => setShowModal(true)} className="btn-primary">
          <Plus className="w-4 h-4 inline mr-2" />
          New Request
        </button>
      </div>

      {/* Filters */}
      <div className="glass-card p-4">
        <div className="flex items-center gap-4">
          <Filter className="w-5 h-5 text-gray-500" />
          <div className="flex gap-2 flex-wrap">
            {[
              "all",
              "New",
              "In Progress",
              "Repaired",
              "Scrap",
            ].map((stage) => (
              <button
                key={stage}
                onClick={() => setFilterStage(stage)}
                className={`px-4 py-2 rounded-lg transition-all ${
                  filterStage === stage
                    ? "bg-purple-600 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}>
                {stage}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Requests List */}
      <div className="space-y-4">
        {filteredRequests.map((item) => (
          <div
            key={item.id}
            className="glass-card p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-4 flex-1">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <Wrench className="w-6 h-6 text-purple-600" />
                </div>

                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-bold text-gray-900">
                      {equipment.find((e) => e.id === item.equipment_id)
                        ?.name || "Unknown Equipment"}
                    </h3>
                    <span className={`badge ${getStageBadge(item.stage)}`}>
                      {item.stage}
                    </span>
                    <span
                      className={`badge ${getPriorityBadge(item.priority)}`}>
                      {item.priority}
                    </span>
                  </div>

                  <p className="text-gray-600 mb-3">{item.description}</p>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                    <div>
                      <span className="text-gray-500">Type:</span>
                      <span className="ml-2 font-medium capitalize">
                        {item.request_type}
                      </span>
                    </div>
                    {item.team_name && (
                      <div>
                        <span className="text-gray-500">Team:</span>
                        <span className="ml-2 font-medium">
                          {item.team_name}
                        </span>
                      </div>
                    )}
                    {item.scheduled_date && (
                      <div>
                        <span className="text-gray-500">Scheduled:</span>
                        <span className="ml-2 font-medium">
                          {new Date(item.scheduled_date).toLocaleDateString()}
                        </span>
                      </div>
                    )}
                    {item.completed_date && (
                      <div>
                        <span className="text-gray-500">Completed:</span>
                        <span className="ml-2 font-medium">
                          {new Date(item.completed_date).toLocaleDateString()}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex gap-2 ml-4">
                <button
                  onClick={() => handleEdit(item)}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                  <Edit2 className="w-4 h-4 text-gray-600" />
                </button>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="p-2 hover:bg-red-50 rounded-lg transition-colors">
                  <Trash2 className="w-4 h-4 text-red-600" />
                </button>
              </div>
            </div>
          </div>
        ))}

        {filteredRequests.length === 0 && (
          <div className="text-center py-12 glass-card">
            <Wrench className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No requests found</p>
            <button
              onClick={() => setShowModal(true)}
              className="btn-primary mt-4">
              Create your first request
            </button>
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900">
                {editingItem ? "Edit Request" : "New Maintenance Request"}
              </h2>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Equipment *
                  </label>
                  <select
                    required
                    className="input-field"
                    value={formData.equipment_id}
                    onChange={(e) =>
                      setFormData({ ...formData, equipment_id: e.target.value })
                    }>
                    <option value="">Select Equipment</option>
                    {equipment.map((item) => (
                      <option key={item.id} value={item.id}>
                        {item.name} - {item.category}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Request Type *
                  </label>
                  <select
                    className="input-field"
                    value={formData.request_type}
                    onChange={(e) =>
                      setFormData({ ...formData, request_type: e.target.value })
                    }>
                    <option value="Corrective">Corrective</option>
                    <option value="Preventive">Preventive</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Priority *
                  </label>
                  <select
                    className="input-field"
                    value={formData.priority}
                    onChange={(e) =>
                      setFormData({ ...formData, priority: e.target.value })
                    }>
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                    <option value="Critical">Critical</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Stage
                  </label>
                  <select
                    className="input-field"
                    value={formData.stage}
                    onChange={(e) =>
                      setFormData({ ...formData, stage: e.target.value })
                    }>
                    <option value="New">New</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Repaired">Repaired</option>
                    <option value="Scrap">Scrap</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Scheduled Date
                  </label>
                  <input
                    type="date"
                    className="input-field"
                    value={formData.scheduled_date}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        scheduled_date: e.target.value,
                      })
                    }
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description *
                </label>
                <textarea
                  required
                  className="input-field"
                  rows="4"
                  value={formData.description}
                  onChange={(e) =>
                    setFormData({ ...formData, description: e.target.value })
                  }
                  placeholder="Describe the issue or maintenance needed..."
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">
                  {editingItem ? "Update Request" : "Create Request"}
                </button>
                <button
                  type="button"
                  onClick={closeModal}
                  className="btn-secondary flex-1">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Requests;
