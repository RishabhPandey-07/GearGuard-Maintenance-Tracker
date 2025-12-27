import { useState, useMemo } from "react";
import { useApp } from "../context/AppContext";
import {
  Calendar as CalendarIcon,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import {
  startOfMonth,
  endOfMonth,
  eachDayOfInterval,
  format,
  isSameMonth,
  isSameDay,
  addMonths,
  subMonths,
} from "date-fns";

const Calendar = () => {
  const { requests, equipment } = useApp();
  const [currentDate, setCurrentDate] = useState(new Date());

  const preventiveRequests = useMemo(() => {
    return requests.filter((r) => r.request_type === "Preventive");
  }, [requests]);

  const monthStart = startOfMonth(currentDate);
  const monthEnd = endOfMonth(currentDate);
  const daysInMonth = eachDayOfInterval({ start: monthStart, end: monthEnd });

  const getRequestsForDay = (day) => {
    return preventiveRequests.filter((r) => {
      if (!r.scheduled_date) return false;
      return isSameDay(new Date(r.scheduled_date), day);
    });
  };

  const previousMonth = () => {
    setCurrentDate(subMonths(currentDate, 1));
  };

  const nextMonth = () => {
    setCurrentDate(addMonths(currentDate, 1));
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold gradient-text">
          Maintenance Calendar
        </h1>
        <p className="text-gray-600 mt-1">
          View preventive maintenance schedule
        </p>
      </div>

      {/* Calendar Controls */}
      <div className="glass-card p-4">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">
            {format(currentDate, "MMMM yyyy")}
          </h2>
          <div className="flex gap-2">
            <button onClick={previousMonth} className="btn-secondary">
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button onClick={nextMonth} className="btn-secondary">
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="glass-card p-6">
        {/* Week Days */}
        <div className="grid grid-cols-7 gap-2 mb-4">
          {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
            <div
              key={day}
              className="text-center font-semibold text-gray-700 py-2">
              {day}
            </div>
          ))}
        </div>

        {/* Calendar Days */}
        <div className="grid grid-cols-7 gap-2">
          {daysInMonth.map((day) => {
            const dayRequests = getRequestsForDay(day);
            const isToday = isSameDay(day, new Date());

            return (
              <div
                key={day.toString()}
                className={`min-h-[120px] p-2 border rounded-lg transition-all hover:shadow-md
                  ${isSameMonth(day, currentDate) ? "bg-white" : "bg-gray-50"}
                  ${isToday ? "border-purple-500 border-2" : "border-gray-200"}
                `}>
                <div
                  className={`text-sm font-medium mb-2 ${
                    isToday ? "text-purple-700" : "text-gray-700"
                  }`}>
                  {format(day, "d")}
                </div>

                <div className="space-y-1">
                  {dayRequests.map((request) => (
                    <div
                      key={request.id}
                      className="text-xs p-1 bg-purple-100 text-purple-700 rounded truncate"
                      title={
                        equipment.find((e) => e.id === request.equipment_id)
                          ?.name
                      }>
                      <CalendarIcon className="w-3 h-3 inline mr-1" />
                      {
                        equipment.find((e) => e.id === request.equipment_id)
                          ?.name
                      }
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Legend */}
      <div className="glass-card p-4">
        <h3 className="font-semibold text-gray-900 mb-3">Legend</h3>
        <div className="flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-purple-500 rounded"></div>
            <span className="text-sm text-gray-600">Today</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-purple-100 rounded"></div>
            <span className="text-sm text-gray-600">
              Preventive Maintenance
            </span>
          </div>
        </div>
      </div>

      {/* Upcoming Schedule */}
      <div className="glass-card p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          Upcoming Preventive Maintenance
        </h3>
        {preventiveRequests.length > 0 ? (
          <div className="space-y-3">
            {preventiveRequests
              .filter(
                (r) =>
                  r.scheduled_date && new Date(r.scheduled_date) >= new Date()
              )
              .sort(
                (a, b) =>
                  new Date(a.scheduled_date) - new Date(b.scheduled_date)
              )
              .slice(0, 5)
              .map((request) => (
                <div
                  key={request.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <CalendarIcon className="w-5 h-5 text-purple-600" />
                    <div>
                      <p className="font-medium text-gray-900">
                        {
                          equipment.find((e) => e.id === request.equipment_id)
                            ?.name
                        }
                      </p>
                      <p className="text-sm text-gray-600">
                        {request.description}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">
                      {format(new Date(request.scheduled_date), "MMM dd, yyyy")}
                    </p>
                    <p className="text-xs text-gray-500 capitalize">
                      {request.priority} priority
                    </p>
                  </div>
                </div>
              ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">
            No preventive maintenance scheduled
          </p>
        )}
      </div>
    </div>
  );
};

export default Calendar;
