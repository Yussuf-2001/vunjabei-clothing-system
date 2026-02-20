import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';

const PlaceOrder = ({ user }) => {
  const { productId } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Tunavuta taarifa za bidhaa ili kuonyesha jina na bei
    axios.get(`http://127.0.0.1:8000/api/products/${productId}/`)
      .then(res => setProduct(res.data))
      .catch(err => console.error("Error fetching product:", err));
  }, [productId]);

  const handlePlaceOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Hapa tunatuma data zote (Simu, Address, Quantity) kwenda Django
      await axios.post('http://127.0.0.1:8000/api/place-order/', {
        product_id: productId,
        quantity: parseInt(quantity),
        phone: phone,
        address: address
      });
      alert('Order placed successfully! We will contact you shortly.');
      navigate('/products'); // Tunarudi kwenye bidhaa
    } catch (err) {
      console.error(err);
      // Onyesha error halisi kutoka server au network error
      setError('Failed to place order: ' + (err.response?.data?.error || err.message || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  if (!product) return <div className="p-5 text-center">Loading product details...</div>;

  return (
    <div className="col-md-6 offset-md-3 mt-5">
      <div className="card shadow border-0">
        <div className="card-header text-white" style={{ backgroundColor: '#6f42c1' }}>
          Place Order: <strong>{product.name}</strong>
        </div>
        <div className="card-body">
          {error && <div className="alert alert-danger">{error}</div>}
          
          <div className="text-center mb-3 p-3 bg-light rounded">
             <h4 className="fw-bold" style={{ color: '#dc3545' }}>Price: TSh {parseFloat(product.price).toLocaleString()}</h4>
             <p className="text-muted mb-0">Stock Available: {product.quantity}</p>
          </div>

          <form onSubmit={handlePlaceOrder}>
            <div className="mb-3">
              <label className="form-label fw-bold">Quantity</label>
              <input 
                type="number" 
                className="form-control" 
                min="1" 
                max={product.quantity}
                value={quantity} 
                onChange={(e) => setQuantity(e.target.value)} 
                required 
              />
            </div>
            <div className="mb-3">
              <label className="form-label fw-bold">Phone Number</label>
              <input 
                type="text" 
                className="form-control" 
                placeholder="Enter your contact number"
                value={phone} 
                onChange={(e) => setPhone(e.target.value)} 
                required 
              />
            </div>
            <div className="mb-3">
              <label className="form-label fw-bold">Delivery Address</label>
              <textarea 
                className="form-control" 
                rows="3" 
                placeholder="Enter full delivery address"
                value={address} 
                onChange={(e) => setAddress(e.target.value)} 
                required 
              ></textarea>
            </div>
            <button type="submit" className="btn text-white w-100 py-2 fw-bold" style={{ backgroundColor: '#6f42c1' }} disabled={loading}>
              {loading ? 'Processing...' : 'Confirm Order'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default PlaceOrder;