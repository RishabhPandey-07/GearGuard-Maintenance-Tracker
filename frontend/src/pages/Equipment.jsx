import { useState, useEffect } from "react";
import { Plus, Edit2, Trash2, Filter, Package } from "lucide-react";
import { useApp } from "../context/AppContext";
import { equipmentAPI } from "../api/services";

const Equipment = () => {
  const { equipment, teams, addEquipment, updateEquipment, deleteEquipment } =
    useApp();
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [filterStatus, setFilterStatus] = useState("all");
  const [formData, setFormData] = useState({
    name: "",
    category: "",
    location: "",
    team_id: "",
    status: "Usable",
    purchase_date: "",
    warranty_expiry: "",
    notes: "",
  });

  const filteredEquipment =
    filterStatus === "all"
      ? equipment
      : equipment.filter((item) => item.status === filterStatus);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await updateEquipment(editingItem.id, formData);
      } else {
        await addEquipment(formData);
      }
      closeModal();
    } catch (error) {
      console.error("Error saving equipment:", error);
      alert("Failed to save equipment");
    }
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setFormData({
      name: item.name,
      category: item.category,
      location: item.location,
      team_id: item.team_id || "",
      status: item.status,
      purchase_date: item.purchase_date || "",
      warranty_expiry: item.warranty_expiry || "",
      notes: item.notes || "",
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this equipment?")) {
      try {
        await deleteEquipment(id);
      } catch (error) {
        console.error("Error deleting equipment:", error);
        alert("Failed to delete equipment");
      }
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingItem(null);
    setFormData({
      name: "",
      category: "",
      location: "",
      team_id: "",
      status: "Usable",
      purchase_date: "",
      warranty_expiry: "",
      notes: "",
    });
  };

  const getStatusBadge = (status) => {
    const badges = {
      Usable: "badge-success",
      Scrapped: "badge-danger",
    };
    return badges[status] || "badge-default";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">
            Equipment Management
          </h1>
          <p className="text-gray-600 mt-1">Manage your equipment inventory</p>
        </div>
        <button onClick={() => setShowModal(true)} className="btn-primary">
          <Plus className="w-4 h-4 inline mr-2" />
          Add Equipment
        </button>
      </div>

      {/* Filters */}
      <div className="glass-card p-4">
        <div className="flex items-center gap-4">
          <Filter className="w-5 h-5 text-gray-500" />
          <div className="flex gap-2">
            {["all", "Usable", "Scrapped"].map(
              (status) => (
                <button
                  key={status}
                  onClick={() => setFilterStatus(status)}
                  className={`px-4 py-2 rounded-lg capitalize transition-all ${
                    filterStatus === status
                      ? "bg-purple-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}>
                  {status}
                </button>
              )
            )}
          </div>
        </div>
      </div>

      {/* Equipment Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredEquipment.map((item) => (
          <div
            key={item.id}
            className="glass-card p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Package className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <h3 className="font-bold text-gray-900">{item.name}</h3>
                  <p className="text-sm text-gray-500">{item.category}</p>
                </div>
              </div>
              <span className={`badge ${getStatusBadge(item.status)}`}>
                {item.status}
              </span>
            </div>

            <div className="space-y-2 text-sm mb-4">
              <p className="text-gray-600">
                <strong>Location:</strong> {item.location}
              </p>
              {item.team_name && (
                <p className="text-gray-600">
                  <strong>Team:</strong> {item.team_name}
                </p>
              )}
              {item.purchase_date && (
                <p className="text-gray-600">
                  <strong>Purchased:</strong>{" "}
                  {new Date(item.purchase_date).toLocaleDateString()}
                </p>
              )}
            </div>

            <div className="flex gap-2 pt-4 border-t border-gray-200">
              <button
                onClick={() => handleEdit(item)}
                className="flex-1 btn-secondary text-sm">
                <Edit2 className="w-4 h-4 inline mr-1" />
                Edit
              </button>
              <button
                onClick={() => handleDelete(item.id)}
                className="flex-1 px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-all text-sm font-medium">
                <Trash2 className="w-4 h-4 inline mr-1" />
                Delete
              </button>
            </div>
          </div>
        ))}

        {filteredEquipment.length === 0 && (
          <div className="col-span-full text-center py-12 glass-card">
            <Package className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No equipment found</p>
            <button
              onClick={() => setShowModal(true)}
              className="btn-primary mt-4">
              Add your first equipment
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
                {editingItem ? "Edit Equipment" : "Add New Equipment"}
              </h2>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Equipment Name *
                  </label>
                  <input
                    type="text"
                    required
                    className="input-field"
                    value={formData.name}
                    onChange={(e) =>
                      setFormData({ ...formData, name: e.target.value })
                    }
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Category *
                  </label>
                  <input
                    type="text"
                    required
                    className="input-field"
                    value={formData.category}
                    onChange={(e) =>
                      setFormData({ ...formData, category: e.target.value })
                    }
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Location *
                  </label>
                  <input
                    type="text"
                    required
                    className="input-field"
                    value={formData.location}
                    onChange={(e) =>
                      setFormData({ ...formData, location: e.target.value })
                    }
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Team
                  </label>
                  <select
                    className="input-field"
                    value={formData.team_id}
                    onChange={(e) =>
                      setFormData({ ...formData, team_id: e.target.value })
                    }>
                    <option value="">No Team</option>
                    {teams.map((team) => (
                      <option key={team.id} value={team.id}>
                        {team.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Status
                  </label>
                  <select
                    className="input-field"
                    value={formData.status}
                    onChange={(e) =>
                      setFormData({ ...formData, status: e.target.value })
                    }>
                    <option value="Usable">Usable</option>
                    <option value="Scrapped">Scrapped</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Purchase Date
                  </label>
                  <input
                    type="date"
                    className="input-field"
                    value={formData.purchase_date}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        purchase_date: e.target.value,
                      })
                    }
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Warranty Expiry
                  </label>
                  <input
                    type="date"
                    className="input-field"
                    value={formData.warranty_expiry}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        warranty_expiry: e.target.value,
                      })
                    }
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Notes
                </label>
                <textarea
                  className="input-field"
                  rows="3"
                  value={formData.notes}
                  onChange={(e) =>
                    setFormData({ ...formData, notes: e.target.value })
                  }
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">
                  {editingItem ? "Update Equipment" : "Add Equipment"}
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

export default Equipment;
