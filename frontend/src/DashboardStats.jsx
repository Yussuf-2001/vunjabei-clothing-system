import React, { useState, useEffect } from 'react';
import api from './api';
        
const DashboardStats = () => {
  const [stats, setStats] = useState({
    products: 0,
    customers: 0,
    sales: 0,
    revenue: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [productsRes, customersRes, salesRes] = await Promise.all([
          api.get('products/').catch(() => ({ data: [] })),
          api.get('customers/').catch(() => ({ data: [] })),
          api.get('sales/').catch(() => ({ data: [] }))
        ]);

        const salesData = Array.isArray(salesRes.data) ? salesRes.data : (salesRes.data.results || []);
        const productsCount = Array.isArray(productsRes.data) ? productsRes.data.length : (productsRes.data.count || 0);
        const customersCount = Array.isArray(customersRes.data) ? customersRes.data.length : (customersRes.data.count || 0);
        const totalRevenue = salesData.reduce((sum, sale) => sum + parseFloat(sale.total_amount || 0), 0);

        setStats({
          products: productsCount,
          customers: customersCount,
          sales: salesData.length,
          revenue: totalRevenue
        });
        setLoading(false);
      } catch (error) {
        console.error("Error loading dashboard stats:", error);
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return <div className="d-flex justify-content-center align-items-center h-100"><h2>Loading Stats...</h2></div>;
  }

  return (
    <div className="p-4">
      <h2 className="mb-4 fw-bold text-secondary">Dashboard Overview</h2>
      <div className="row g-4">
        <div className="col-md-3">
          <div className="card p-3 border-0 shadow-sm border-start border-primary border-5">
            <h6 className="text-muted text-uppercase">All Products</h6>
            <h3 className="fw-bold text-primary">{stats.products}</h3>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card p-3 border-0 shadow-sm border-start border-success border-5">
            <h6 className="text-muted text-uppercase">Total Sales</h6>
            <h3 className="fw-bold text-success">{stats.sales}</h3>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card p-3 border-0 shadow-sm border-start border-warning border-5">
            <h6 className="text-muted text-uppercase">Customers</h6>
            <h3 className="fw-bold text-warning">{stats.customers}</h3>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card p-3 border-0 shadow-sm border-start border-danger border-5">
            <h6 className="text-muted text-uppercase">Revenue (TSh)</h6>
            <h3 className="fw-bold text-danger">{stats.revenue.toLocaleString()}</h3>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardStats
