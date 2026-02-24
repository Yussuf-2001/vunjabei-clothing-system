import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import api from './api';

const ProductDetailPage = ({ user }) => {
    const { productId } = useParams();
    const navigate = useNavigate();
    const [product, setProduct] = useState(null);
    const [quantity, setQuantity] = useState(1);
    const [phone, setPhone] = useState('');
    const [address, setAddress] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const res = await api.get(`products/${productId}/`);
                setProduct(res.data);
            } catch (error) {
                console.error("Failed to fetch product", error);
            }
        };
        fetchProduct();
    }, [productId]);

    const handlePlaceOrder = async (e) => {
        e.preventDefault();
        if (!user) {
            setError('You must be logged in to place an order.');
            return;
        }
        setError('');
        try {
            await api.post('place-order/', {
                product_id: productId,
                quantity: Number(quantity),
                phone: phone,
                address: address
            });
            alert('Order placed successfully!');
            navigate('/customer/my-orders');
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to place order.');
        }
    };

    if (!product) return <div className="text-center p-5"><h2>Loading...</h2></div>;

    return (
        <div className="row g-4">
            <div className="col-md-6">
                <div className="product-detail-media">
                    <img src={product.image || '/media/product_images/default-product.svg'} className="product-detail-image" alt={product.name} />
                </div>
            </div>
            <div className="col-md-6">
                <h2>{product.name}</h2>
                <p className="text-muted">{product.category_name}</p>
                <p className="fs-3 fw-bold text-danger">TSh {parseFloat(product.price).toLocaleString()}</p>
                <p><strong>Stock:</strong> {product.quantity > 0 ? `${product.quantity} available` : 'Out of Stock'}</p>
                <hr />
                <h4>Place Your Order</h4>
                {error && <div className="alert alert-danger">{error}</div>}
                <form onSubmit={handlePlaceOrder}>
                    <div className="mb-3">
                        <label className="form-label">Quantity</label>
                        <input type="number" className="form-control" value={quantity} onChange={e => setQuantity(e.target.value)} min="1" max={product.quantity} required />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Phone Number</label>
                        <input type="tel" className="form-control" value={phone} onChange={e => setPhone(e.target.value)} placeholder="e.g., 0712345678" required />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Delivery Address</label>
                        <textarea className="form-control" value={address} onChange={e => setAddress(e.target.value)} rows="3" placeholder="Full address for delivery" required></textarea>
                    </div>
                    <button type="submit" className="btn btn-primary w-100 btn-lg" disabled={product.quantity === 0}>
                        {product.quantity > 0 ? 'Place Order' : 'Out of Stock'}
                    </button>
                    {!user && <p className="text-warning mt-2">Please <Link to="/login">login</Link> to place an order.</p>}
                </form>
            </div>
        </div>
    );
};

export default ProductDetailPage;
