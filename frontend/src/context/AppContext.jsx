import { createContext, useContext, useState, useEffect } from "react";
import { equipmentAPI, requestsAPI, teamsAPI } from "../api/services";

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within AppProvider");
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [equipment, setEquipment] = useState([]);
  const [requests, setRequests] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch initial data
  const fetchData = async () => {
    try {
      setLoading(true);
      const [equipmentRes, requestsRes, teamsRes] = await Promise.all([
        equipmentAPI.getAll(),
        requestsAPI.getAll(),
        teamsAPI.getAll(),
      ]);

      setEquipment(equipmentRes.data);
      setRequests(requestsRes.data);
      setTeams(teamsRes.data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Equipment actions
  const addEquipment = async (data) => {
    try {
      const response = await equipmentAPI.create(data);
      setEquipment([...equipment, response.data]);
      return response.data;
    } catch (err) {
      throw err;
    }
  };

  const updateEquipment = async (id, data) => {
    try {
      const response = await equipmentAPI.update(id, data);
      setEquipment(
        equipment.map((item) => (item.id === id ? response.data : item))
      );
      return response.data;
    } catch (err) {
      throw err;
    }
  };

  const deleteEquipment = async (id) => {
    try {
      await equipmentAPI.delete(id);
      setEquipment(equipment.filter((item) => item.id !== id));
    } catch (err) {
      throw err;
    }
  };

  // Request actions
  const addRequest = async (data) => {
    try {
      const response = await requestsAPI.create(data);
      setRequests([...requests, response.data]);
      return response.data;
    } catch (err) {
      throw err;
    }
  };

  const updateRequest = async (id, data) => {
    try {
      const response = await requestsAPI.update(id, data);
      setRequests(
        requests.map((item) => (item.id === id ? response.data : item))
      );

      // If scrap logic triggered, refresh equipment
      if (data.stage === "Scrap") {
        fetchData();
      }

      return response.data;
    } catch (err) {
      throw err;
    }
  };

  const deleteRequest = async (id) => {
    try {
      await requestsAPI.delete(id);
      setRequests(requests.filter((item) => item.id !== id));
    } catch (err) {
      throw err;
    }
  };

  const value = {
    equipment,
    requests,
    teams,
    loading,
    error,
    fetchData,
    addEquipment,
    updateEquipment,
    deleteEquipment,
    addRequest,
    updateRequest,
    deleteRequest,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
