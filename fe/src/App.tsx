import { useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface Prediction {
  predicted_price_aed: number;
  rental_yield_percent: number;
  roi_5yr_percent: number;
}

function App() {
  const [formData, setFormData] = useState({
    area: 'Marina',
    property_type: 'Apartment',
    size_sqft: 1000,
    bedrooms: 2
  });
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'size_sqft' || name === 'bedrooms' ? Number(value) : value
    }));
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch prediction');
      }
      
      const data = await response.json();
      setPrediction(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred server-side.');
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-AE', { style: 'currency', currency: 'AED', maximumFractionDigits: 0 }).format(value);
  };

  return (
    <div className="min-h-screen p-8 flex flex-col items-center">
      
      {/* Header */}
      <header className="mb-12 text-center mt-10">
        <h1 className="text-5xl font-extrabold tracking-tight mb-4">
          <span className="gradient-text">DubaiPropAI</span> Predictor
        </h1>
        <p className="text-slate-400 max-w-xl text-lg">
          Simulate real estate investments across Dubai using our XGBoost machine learning model.
        </p>
      </header>

      <main className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Input Form Column */}
        <section className="glass-panel">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <svg className="w-6 h-6 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            Property Details
          </h2>
          <form onSubmit={handlePredict} className="space-y-6">
            
            <div>
              <label className="input-label">Location Area</label>
              <select name="area" value={formData.area} onChange={handleChange} className="input-field">
                <option value="Marina">Dubai Marina</option>
                <option value="Downtown">Downtown Dubai</option>
                <option value="JVC">Jumeirah Village Circle (JVC)</option>
                <option value="Business Bay">Business Bay</option>
                <option value="Palm Jumeirah">Palm Jumeirah</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="input-label">Property Type</label>
                <select name="property_type" value={formData.property_type} onChange={handleChange} className="input-field">
                  <option value="Apartment">Apartment</option>
                  <option value="Villa">Villa</option>
                  <option value="Townhouse">Townhouse</option>
                </select>
              </div>
              
              <div>
                <label className="input-label">Bedrooms</label>
                <input type="number" name="bedrooms" min="1" max="10" value={formData.bedrooms} onChange={handleChange} className="input-field" required />
              </div>
            </div>

            <div>
              <label className="input-label">Size (Sq.Ft)</label>
              <input type="number" name="size_sqft" min="100" max="20000" step="50" value={formData.size_sqft} onChange={handleChange} className="input-field" required />
            </div>

            <button type="submit" disabled={loading} className="btn-primary flex items-center justify-center gap-2">
              {loading ? (
                <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              ) : (
                <>Generate AI Prediction</>
              )}
            </button>
            {error && <p className="text-red-400 text-sm">{error}</p>}
          </form>
        </section>

        {/* Results Column */}
        <section className="flex flex-col gap-6">
          <div className="glass-panel flex-1 flex flex-col justify-center relative overflow-hidden">
             {/* Decorative blob */}
             <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/20 rounded-full blur-3xl -mr-16 -mt-16"></div>
             
             <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-widest mb-2">Estimated Value</h3>
             <div className="text-5xl font-bold text-white mb-1">
               {prediction ? formatCurrency(prediction.predicted_price_aed) : '---'}
             </div>
             <p className="text-indigo-300 text-sm">Predicted using XGBoost Regressor</p>
          </div>

          <div className="grid grid-cols-2 gap-6 h-48">
            <div className="glass-panel flex flex-col justify-center relative overflow-hidden group">
               <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-400 to-emerald-600 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
               <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-widest mb-3">Rental Yield</h3>
               <div className="text-4xl font-bold text-white">
                 {prediction ? `${prediction.rental_yield_percent.toFixed(2)}%` : '---'}
               </div>
            </div>

            <div className="glass-panel flex flex-col justify-center relative overflow-hidden group">
               <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-blue-400 to-cyan-600 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
               <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-widest mb-3">5-Year ROI</h3>
               <div className="text-4xl font-bold text-white">
                 {prediction ? `${prediction.roi_5yr_percent.toFixed(2)}%` : '---'}
               </div>
            </div>
          </div>

          {/* Dynamic Map Integration */}
          <div className="glass-panel flex-1 p-0 relative overflow-hidden min-h-[250px] border border-slate-700/50">
             <iframe
               title="Property Location View"
               width="100%"
               height="100%"
               style={{ border: 0, minHeight: '250px', background: 'transparent' }}
               loading="lazy"
               src={`https://maps.google.com/maps?q=${encodeURIComponent(formData.area + ', Dubai')}&t=&z=13&ie=UTF8&iwloc=&output=embed`}
             ></iframe>
          </div>
        </section>

      </main>
    </div>
  );
}

export default App;
