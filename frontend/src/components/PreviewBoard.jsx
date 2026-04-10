import React from 'react';
import { Network, Check, ExternalLink, AlertCircle } from 'lucide-react';

export default function PreviewBoard({ previews, setPreviews, onPublish, isPublishing, publishStatus }) {
  if (!previews) {
    return (
      <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100%', opacity: 0.5 }}>
        <Network size={48} color="hsl(var(--text-secondary))" style={{ marginBottom: '1rem' }} />
        <h3>Awaiting Idea</h3>
        <p style={{ textAlign: 'center', marginTop: '0.5rem' }}>Your AI tailored posts will appear here for review.</p>
      </div>
    );
  }

  const handleEdit = (platform, newText) => {
    setPreviews({
      ...previews,
      [platform]: newText
    });
  };

  return (
    <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
      <div className="preview-header">
        <div>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Check size={20} color="hsl(150, 80%, 40%)" />
            Review & Edit
          </h2>
          <p style={{ fontSize: '0.9rem', marginTop: '0.2rem' }}>You can edit the AI generated text below before publishing.</p>
        </div>
        
        <button 
          className="btn-primary" 
          style={{ width: 'auto', padding: '0.5rem 1.5rem', background: 'linear-gradient(135deg, hsl(150, 80%, 40%), hsl(160, 80%, 30%))' }}
          onClick={onPublish}
          disabled={isPublishing || publishStatus === 'success'}
        >
          {isPublishing ? 'Publishing...' : publishStatus === 'success' ? 'Published!' : 'Approve & Publish'}
        </button>
      </div>

      {publishStatus === 'error' && (
        <div style={{ padding: '1rem', backgroundColor: 'rgba(255,50,50,0.1)', border: '1px solid red', borderRadius: '8px', marginBottom: '1rem', display: 'flex', gap: '0.5rem', color: 'hsl(0, 80%, 70%)' }}>
          <AlertCircle size={20} /> Failed to publish. Please check the backend logs.
        </div>
      )}

      {publishStatus === 'success' && (
        <div style={{ padding: '1rem', backgroundColor: 'rgba(50,255,100,0.1)', border: '1px solid green', borderRadius: '8px', marginBottom: '1rem', display: 'flex', gap: '0.5rem', color: 'hsl(150, 80%, 60%)' }}>
          <Check size={20} /> Successfully scheduled on Ayrshare!
        </div>
      )}

      <div className="preview-grid">
        {Object.entries(previews).map(([platform, text]) => (
          <div key={platform} className="preview-card">
            <div className="preview-platform-header">
              <span style={{ textTransform: 'capitalize' }}>{platform}</span>
            </div>
            <textarea 
              className="preview-textarea"
              value={text}
              onChange={(e) => handleEdit(platform, e.target.value)}
              disabled={isPublishing || publishStatus === 'success'}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
