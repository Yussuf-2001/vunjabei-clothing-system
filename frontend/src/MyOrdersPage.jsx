import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from './api';

const MyOrdersPage = ({ user }) => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchOrders = async () => {
            if (!user) {
                setLoading(false);
                return;
            }
            try {
                const res = await api.get('my-orders/', { params: { username: user.username } });
                setOrders(res.data);
                setLoading(false);
            } catch (error) {
                console.error("Failed to fetch orders", error);
                setLoading(false);
            }
        };
        fetchOrders();
    }, [user]);

    if (loading) return <div className="text-center p-5"><h2>Loading your orders...</h2></div>;

    return (
        <div>
            <h2 className="mb-4">My Order History</h2>
            {orders.length === 0 ? (
                <div className="alert alert-info">You have no orders. <Link to="/customer/products">Start shopping!</Link></div>
            ) : (
                <div className="card shadow-sm">
                    <div className="table-responsive">
                        <table className="table table-hover mb-0">
                            <thead>
                                <tr><th>Order ID</th><th>Product</th><th>Quantity</th><th>Total</th><th>Date</th><th>Status</th></tr>
                            </thead>
                            <tbody>
                                {orders.map(order => (
                                    <tr key={order.id}>
                                        <td>#{order.id}</td>
                                        <td>{order.product_name}</td>
                                        <td>{order.quantity}</td>
                                        <td>TSh {parseFloat(order.total_price).toLocaleString()}</td>
                                        <td>{new Date(order.date).toLocaleString()}</td>
                                        <td><span className={`badge ${order.status === 'Pending' ? 'bg-warning' : 'bg-success'}`}>{order.status}</span></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MyOrdersPage;
