import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Package,
  Wrench,
  KanbanSquare,
  Calendar,
  Users,
} from "lucide-react";

const Layout = ({ children }) => {
  const location = useLocation();

  const navigation = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard },
    { name: "Equipment", href: "/equipment", icon: Package },
    { name: "Requests", href: "/requests", icon: Wrench },
    { name: "Kanban Board", href: "/kanban", icon: KanbanSquare },
    { name: "Calendar", href: "/calendar", icon: Calendar },
    { name: "Teams", href: "/teams", icon: Users },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-purple-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-md border-b border-gray-200 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-purple-800 rounded-lg flex items-center justify-center shadow-lg">
                <Wrench className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold gradient-text">GearGuard</h1>
                <p className="text-xs text-gray-500">
                  Maintenance Management System
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-700">Admin User</p>
                <p className="text-xs text-gray-500">Administrator</p>
              </div>
              <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-purple-800 rounded-full flex items-center justify-center text-white font-semibold shadow-md">
                A
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 shadow-sm sticky top-[73px] z-40">
        <div className="container mx-auto px-4">
          <div className="flex gap-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;

              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    flex items-center gap-2 px-4 py-3 text-sm font-medium transition-all duration-200
                    ${
                      isActive
                        ? "text-purple-700 border-b-2 border-purple-700 bg-purple-50"
                        : "text-gray-600 hover:text-purple-600 hover:bg-purple-50/50"
                    }
                  `}>
                  <Icon className="w-4 h-4" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">{children}</main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="container mx-auto px-4 py-4">
          <div className="text-center text-sm text-gray-500">
            © 2025 GearGuard. Built with React + Flask. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
