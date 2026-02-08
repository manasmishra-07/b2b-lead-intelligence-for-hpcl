import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, BarChart3 } from 'lucide-react';
import { Users } from 'lucide-react';


function Sidebar({ darkMode }) {
  

// Add to navItems array:
const navItems = [
  { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/leads', icon: FileText, label: 'Leads' },
//   { path: '/sales-officers', icon: Users, label: 'Sales Officers' },
  { path: '/analytics', icon: BarChart3, label: 'Analytics' },
];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-white rounded-lg flex items-center justify-center">
            <span className="text-2xl font-bold text-hpcl-blue">HP</span>
          </div>
          <div>
            <h2 className="text-xl font-bold">HPCL</h2>
            <p className="text-xs text-blue-200">Lead Intelligence</p>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `nav-link ${isActive ? 'active' : ''}`
            }
          >
            <item.icon className="w-5 h-5" />
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-blue-700">
        <p className="text-xs text-blue-200 text-center">
          © 2026 HPCL Direct Sales
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;