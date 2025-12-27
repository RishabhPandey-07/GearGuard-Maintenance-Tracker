import { useState } from "react";
import { useApp } from "../context/AppContext";
import { Wrench } from "lucide-react";

const Kanban = () => {
  const { requests, equipment, updateRequest } = useApp();
  const [draggedItem, setDraggedItem] = useState(null);

  const stages = ["New", "In Progress", "Repaired", "Scrap"];

  const handleDragStart = (item) => {
    setDraggedItem(item);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = async (stage) => {
    if (draggedItem && draggedItem.stage !== stage) {
      try {
        await updateRequest(draggedItem.id, { ...draggedItem, stage });
        setDraggedItem(null);
      } catch (error) {
        console.error("Error updating request:", error);
      }
    }
  };

  const getRequestsByStage = (stage) => {
    return requests.filter((r) => r.stage === stage);
  };

  const getPriorityColor = (priority) => {
    const colors = {
      Low: "border-l-blue-500",
      Medium: "border-l-yellow-500",
      High: "border-l-orange-500",
      Critical: "border-l-red-500",
    };
    return colors[priority] || "border-l-gray-500";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold gradient-text">Kanban Board</h1>
        <p className="text-gray-600 mt-1">
          Drag and drop requests between stages
        </p>
      </div>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stages.map((stage) => {
          const stageRequests = getRequestsByStage(stage);

          return (
            <div
              key={stage}
              className="glass-card p-4"
              onDragOver={handleDragOver}
              onDrop={() => handleDrop(stage)}>
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-bold text-gray-900">{stage}</h2>
                <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-medium">
                  {stageRequests.length}
                </span>
              </div>

              <div className="space-y-3 min-h-[500px]">
                {stageRequests.map((item) => (
                  <div
                    key={item.id}
                    draggable
                    onDragStart={() => handleDragStart(item)}
                    className={`bg-white p-4 rounded-lg border-l-4 ${getPriorityColor(
                      item.priority
                    )} 
                               shadow-md hover:shadow-lg cursor-move transition-all`}>
                    <div className="flex items-start gap-3 mb-2">
                      <div className="w-8 h-8 bg-purple-100 rounded flex items-center justify-center flex-shrink-0">
                        <Wrench className="w-4 h-4 text-purple-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-gray-900 text-sm truncate">
                          {equipment.find((e) => e.id === item.equipment_id)
                            ?.name || "Unknown"}
                        </h3>
                        <p className="text-xs text-gray-500 capitalize">
                          {item.request_type}
                        </p>
                      </div>
                    </div>

                    <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                      {item.description}
                    </p>

                    <div className="flex items-center justify-between">
                      <span
                        className={`text-xs px-2 py-1 rounded-full font-medium capitalize
                        ${
                          item.priority === "Critical"
                            ? "bg-red-100 text-red-700"
                            : ""
                        }
                        ${
                          item.priority === "High"
                            ? "bg-orange-100 text-orange-700"
                            : ""
                        }
                        ${
                          item.priority === "Medium"
                            ? "bg-yellow-100 text-yellow-700"
                            : ""
                        }
                        ${
                          item.priority === "Low"
                            ? "bg-blue-100 text-blue-700"
                            : ""
                        }
                      `}>
                        {item.priority}
                      </span>
                      {item.team_name && (
                        <span className="text-xs text-gray-500 truncate ml-2">
                          {item.team_name}
                        </span>
                      )}
                    </div>
                  </div>
                ))}

                {stageRequests.length === 0 && (
                  <div className="text-center py-8 text-gray-400 text-sm">
                    Drop items here
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Kanban;
