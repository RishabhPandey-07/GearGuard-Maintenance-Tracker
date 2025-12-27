import { useState, useEffect } from "react";
import { Plus, Edit2, Trash2, Users as UsersIcon, User } from "lucide-react";
import { useApp } from "../context/AppContext";
import { teamsAPI } from "../api/services";

const Teams = () => {
  const { teams, fetchData } = useApp();
  const [members, setMembers] = useState([]);
  const [showTeamModal, setShowTeamModal] = useState(false);
  const [showMemberModal, setShowMemberModal] = useState(false);
  const [editingTeam, setEditingTeam] = useState(null);
  const [editingMember, setEditingMember] = useState(null);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [teamForm, setTeamForm] = useState({ name: "", description: "" });
  const [memberForm, setMemberForm] = useState({
    team_id: "",
    name: "",
    role: "",
    email: "",
    phone: "",
  });

  useEffect(() => {
    fetchMembers();
  }, []);

  const fetchMembers = async () => {
    try {
      const response = await teamsAPI.getAllMembers();
      setMembers(response.data);
    } catch (error) {
      console.error("Error fetching members:", error);
    }
  };

  const handleTeamSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingTeam) {
        // Update not implemented in API, skip for now
        alert("Team update not implemented");
      } else {
        await teamsAPI.create(teamForm);
      }
      await fetchData();
      closeTeamModal();
    } catch (error) {
      console.error("Error saving team:", error);
      alert("Failed to save team");
    }
  };

  const handleMemberSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingMember) {
        await teamsAPI.updateMember(editingMember.id, memberForm);
      } else {
        await teamsAPI.createMember(memberForm);
      }
      await fetchMembers();
      closeMemberModal();
    } catch (error) {
      console.error("Error saving member:", error);
      alert("Failed to save member");
    }
  };

  const handleDeleteTeam = async (id) => {
    if (window.confirm("Are you sure? This will delete all team members!")) {
      try {
        await teamsAPI.delete(id);
        await fetchData();
        await fetchMembers();
      } catch (error) {
        console.error("Error deleting team:", error);
        alert("Failed to delete team");
      }
    }
  };

  const handleDeleteMember = async (id) => {
    if (window.confirm("Are you sure you want to delete this member?")) {
      try {
        await teamsAPI.deleteMember(id);
        await fetchMembers();
      } catch (error) {
        console.error("Error deleting member:", error);
        alert("Failed to delete member");
      }
    }
  };

  const editMember = (member) => {
    setEditingMember(member);
    setMemberForm({
      team_id: member.team_id,
      name: member.name,
      role: member.role,
      email: member.email,
      phone: member.phone,
    });
    setShowMemberModal(true);
  };

  const closeTeamModal = () => {
    setShowTeamModal(false);
    setEditingTeam(null);
    setTeamForm({ name: "", description: "" });
  };

  const closeMemberModal = () => {
    setShowMemberModal(false);
    setEditingMember(null);
    setMemberForm({ team_id: "", name: "", role: "", email: "", phone: "" });
  };

  const getTeamMembers = (teamId) => {
    return members.filter((m) => m.team_id === teamId);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Teams & Members</h1>
          <p className="text-gray-600 mt-1">Manage your maintenance teams</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowMemberModal(true)}
            className="btn-secondary">
            <User className="w-4 h-4 inline mr-2" />
            Add Member
          </button>
          <button
            onClick={() => setShowTeamModal(true)}
            className="btn-primary">
            <Plus className="w-4 h-4 inline mr-2" />
            Add Team
          </button>
        </div>
      </div>

      {/* Teams Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {teams.map((team) => {
          const teamMembers = getTeamMembers(team.id);

          return (
            <div key={team.id} className="glass-card p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <UsersIcon className="w-6 h-6 text-purple-600" />
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900">{team.name}</h3>
                    <p className="text-sm text-gray-500">
                      {teamMembers.length} members
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleDeleteTeam(team.id)}
                  className="p-2 hover:bg-red-50 rounded-lg transition-colors">
                  <Trash2 className="w-4 h-4 text-red-600" />
                </button>
              </div>

              <p className="text-gray-600 text-sm mb-4">{team.description}</p>

              {/* Team Members */}
              <div className="space-y-2">
                <h4 className="text-sm font-semibold text-gray-700 mb-2">
                  Members
                </h4>
                {teamMembers.length > 0 ? (
                  teamMembers.map((member) => (
                    <div
                      key={member.id}
                      className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {member.name}
                        </p>
                        <p className="text-xs text-gray-500">{member.role}</p>
                      </div>
                      <div className="flex gap-1">
                        <button
                          onClick={() => editMember(member)}
                          className="p-1 hover:bg-white rounded transition-colors">
                          <Edit2 className="w-3 h-3 text-gray-600" />
                        </button>
                        <button
                          onClick={() => handleDeleteMember(member.id)}
                          className="p-1 hover:bg-white rounded transition-colors">
                          <Trash2 className="w-3 h-3 text-red-600" />
                        </button>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-gray-500 italic">No members yet</p>
                )}
              </div>
            </div>
          );
        })}

        {teams.length === 0 && (
          <div className="col-span-full text-center py-12 glass-card">
            <UsersIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No teams found</p>
            <button
              onClick={() => setShowTeamModal(true)}
              className="btn-primary mt-4">
              Create your first team
            </button>
          </div>
        )}
      </div>

      {/* Team Modal */}
      {showTeamModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900">Add New Team</h2>
            </div>

            <form onSubmit={handleTeamSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Team Name *
                </label>
                <input
                  type="text"
                  required
                  className="input-field"
                  value={teamForm.name}
                  onChange={(e) =>
                    setTeamForm({ ...teamForm, name: e.target.value })
                  }
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description *
                </label>
                <textarea
                  required
                  className="input-field"
                  rows="3"
                  value={teamForm.description}
                  onChange={(e) =>
                    setTeamForm({ ...teamForm, description: e.target.value })
                  }
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">
                  Create Team
                </button>
                <button
                  type="button"
                  onClick={closeTeamModal}
                  className="btn-secondary flex-1">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Member Modal */}
      {showMemberModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900">
                {editingMember ? "Edit Member" : "Add New Member"}
              </h2>
            </div>

            <form onSubmit={handleMemberSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Team *
                </label>
                <select
                  required
                  className="input-field"
                  value={memberForm.team_id}
                  onChange={(e) =>
                    setMemberForm({ ...memberForm, team_id: e.target.value })
                  }>
                  <option value="">Select Team</option>
                  {teams.map((team) => (
                    <option key={team.id} value={team.id}>
                      {team.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Name *
                </label>
                <input
                  type="text"
                  required
                  className="input-field"
                  value={memberForm.name}
                  onChange={(e) =>
                    setMemberForm({ ...memberForm, name: e.target.value })
                  }
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Role *
                </label>
                <input
                  type="text"
                  required
                  className="input-field"
                  value={memberForm.role}
                  onChange={(e) =>
                    setMemberForm({ ...memberForm, role: e.target.value })
                  }
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email *
                </label>
                <input
                  type="email"
                  required
                  className="input-field"
                  value={memberForm.email}
                  onChange={(e) =>
                    setMemberForm({ ...memberForm, email: e.target.value })
                  }
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Phone
                </label>
                <input
                  type="tel"
                  className="input-field"
                  value={memberForm.phone}
                  onChange={(e) =>
                    setMemberForm({ ...memberForm, phone: e.target.value })
                  }
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">
                  {editingMember ? "Update Member" : "Add Member"}
                </button>
                <button
                  type="button"
                  onClick={closeMemberModal}
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

export default Teams;
