import Cookies from "js-cookie";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  LineChart,
  Line,
  Tooltip,
} from "recharts";

function Dashboard() {
  const navigate = useNavigate();

  const [darkMode, setDarkMode] = useState(false);
  const [barData, setBarData] = useState([]);
  const [lineData, setLineData] = useState([]);
  const [selectedFeature, setSelectedFeature] = useState("");

  const [filters, setFilters] = useState({
    start_date: "",
    age_group: "",
    gender: "",
  });

  const token = localStorage.getItem("token");

  // 🔐 Logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    Cookies.remove("filters");
    navigate("/");
  };

  // 📊 Fetch Analytics
  const fetchAnalytics = async (
    feature = selectedFeature,
    start_date = filters.start_date,
    age_group = filters.age_group,
    gender = filters.gender
  ) => {
    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/analytics?selected_feature=${feature}&start_date=${start_date}&age_group=${age_group}&gender=${gender}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setBarData(res.data.bar_chart);
      setLineData(res.data.line_chart);
    } catch (err) {
      console.error("Analytics fetch error:", err);
    }
  };

  // 🍪 Restore Filters on Load
  useEffect(() => {
    const saved = Cookies.get("filters");

    if (saved) {
      const parsed = JSON.parse(saved);
      setFilters(parsed);
      fetchAnalytics("", parsed.start_date, parsed.age_group, parsed.gender);
    } else {
      fetchAnalytics();
    }
  }, []);

  // 📊 Bar Click Tracking
  const handleBarClick = async (data) => {
    setSelectedFeature(data.feature_name);

    await axios.post(
      "http://127.0.0.1:8000/track",
      { feature_name: "bar_chart_click" },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    fetchAnalytics(data.feature_name);
  };

  // 🎯 Filter Change Tracking
  const handleFilterChange = async (name, value) => {
    const updated = { ...filters, [name]: value };
    setFilters(updated);

    Cookies.set("filters", JSON.stringify(updated));

    await axios.post(
      "http://127.0.0.1:8000/track",
      { feature_name: name + "_filter" },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    fetchAnalytics(
      selectedFeature,
      updated.start_date,
      updated.age_group,
      updated.gender
    );
  };

  return (
    <div className={`dashboard-container ${darkMode ? "dark" : ""}`}>
      {/* 🔝 Top Bar */}
      <div className="top-bar">
        <h2 className="dashboard-title">Analytics Dashboard</h2>

        <div>
          <button
            className="dark-toggle"
            onClick={() => setDarkMode(!darkMode)}
          >
            {darkMode ? "Light Mode ☀️" : "Dark Mode 🌙"}
          </button>

          <button
            className="logout-btn"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </div>

      {/* 🎛 Filters */}
      <div className="filters">
        <input
          type="date"
          value={filters.start_date}
          onChange={(e) =>
            handleFilterChange("start_date", e.target.value)
          }
        />

        <select
          value={filters.gender}
          onChange={(e) =>
            handleFilterChange("gender", e.target.value)
          }
        >
          <option value="">All Genders</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>

        <select
          value={filters.age_group}
          onChange={(e) =>
            handleFilterChange("age_group", e.target.value)
          }
        >
          <option value="">All Ages</option>
          <option value="<18">&lt;18</option>
          <option value="18-40">18-40</option>
          <option value=">40">&gt;40</option>
        </select>
      </div>

      {/* 📊 Bar Chart */}
      <div className="chart-section">
        <BarChart
          width={900}
          height={380}
          data={barData}
          margin={{ top: 20, right: 40, left: 20, bottom: 100 }}
        >
          <XAxis
            dataKey="feature_name"
            tickFormatter={(value) =>
              value.replace("_filter", "").replace("_click", "")
            }
            
            textAnchor="end"
            interval={0}
            height={80}
            stroke={darkMode ? "#ffffff" : "#000000"}
          />
          <YAxis stroke={darkMode ? "#ffffff" : "#000000"} />
          <Tooltip />
          <Bar
            dataKey="count"
            fill={darkMode ? "#60a5fa" : "#3b82f6"}
            radius={[6, 6, 0, 0]}
            onClick={handleBarClick}
          />
        </BarChart>
      </div>

      {/* 📈 Line Chart */}
      <div className="chart-section">
        <LineChart
          width={900}
          height={380}
          data={lineData}
          margin={{ top: 20, right: 40, left: 20, bottom: 60 }}
        >
          <XAxis
            dataKey="date"
            stroke={darkMode ? "#ffffff" : "#000000"}
          />
          <YAxis stroke={darkMode ? "#ffffff" : "#000000"} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="count"
            stroke={darkMode ? "#34d399" : "#10b981"}
            strokeWidth={3}
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </div>
    </div>
  );
}

export default Dashboard;