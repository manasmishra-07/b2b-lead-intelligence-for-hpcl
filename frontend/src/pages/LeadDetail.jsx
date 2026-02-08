import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft, Building2, MapPin, Clock, Phone, Mail } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

function LeadDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data: lead, isLoading } = useQuery({
    queryKey: ['lead', id],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/leads/${id}`);
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-hpcl-blue border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  if (!lead) {
    return <div className="text-center p-8">Lead not found</div>;
  }

  return (
    <div className="space-y-6">
      <button
        onClick={() => navigate('/leads')}
        className="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-hpcl-blue"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Leads</span>
      </button>

      <div className="bg-gradient-to-r from-hpcl-blue to-hpcl-darkBlue rounded-lg p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">{lead.company?.name || 'Unknown'}</h1>
            <p className="text-blue-100">{lead.company?.industry} • {lead.company?.city}</p>
          </div>
          <div className="text-center bg-white/10 rounded-lg p-6">
            <p className="text-sm text-blue-200 mb-1">Lead Score</p>
            <p className="text-5xl font-bold">{Math.round(lead.lead_score || 0)}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
              <Building2 className="w-5 h-5 mr-2 text-hpcl-blue" />
              Company Information
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Industry</p>
                <p className="font-medium text-gray-900 dark:text-white">{lead.company?.industry || 'N/A'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Location</p>
                <p className="font-medium text-gray-900 dark:text-white flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  {lead.company?.city}, {lead.company?.state}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Signal Context</h2>
            <div className="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 p-4 rounded">
              <p className="text-sm text-gray-700 dark:text-gray-300">{lead.signal_text || 'No signal'}</p>
            </div>
            <div className="mt-4 flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
              <Clock className="w-4 h-4" />
              <span>{new Date(lead.created_at).toLocaleDateString()}</span>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Recommended Products</h2>
            <div className="space-y-4">
              {lead.recommended_products?.map((product, idx) => (
                <div key={idx} className="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-hpcl-blue p-4 rounded">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-bold text-hpcl-blue text-lg">{product.product}</h3>
                    <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
                      {Math.round(product.confidence * 100)}% Match
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-300">{product.reason}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="font-bold text-gray-900 dark:text-white mb-4">Lead Details</h3>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Intent</p>
                <span className="inline-block mt-1 px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm">
                  {lead.intent_strength?.toUpperCase()}
                </span>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400">Status</p>
                <span className="inline-block mt-1 px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                  {lead.status?.toUpperCase()}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
            <h3 className="font-bold text-gray-900 dark:text-white mb-4">Actions</h3>
            <div className="space-y-3">
              <button className="w-full flex items-center justify-center space-x-2 bg-hpcl-blue text-white px-4 py-3 rounded-lg hover:bg-hpcl-darkBlue">
                <Phone className="w-4 h-4" />
                <span>Call Now</span>
              </button>
              <button className="w-full flex items-center justify-center space-x-2 bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-3 rounded-lg">
                <Mail className="w-4 h-4" />
                <span>Email</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LeadDetail;