import React from 'react';
import { PenTool, CheckCircle, Send, Plus } from 'lucide-react';

const platformsList = [
  { id: 'twitter', name: 'Twitter / X', color: 'hsl(203, 89%, 53%)' },
  { id: 'linkedin', name: 'LinkedIn', color: 'hsl(210, 90%, 40%)' },
  { id: 'instagram', name: 'Instagram', color: 'hsl(326, 68%, 53%)' },
  { id: 'facebook', name: 'Facebook', color: 'hsl(214, 89%, 52%)' }
];

export default function PostEditor({ baseText, setBaseText, imageBase64, setImageBase64, platforms, setPlatforms, onGenerate, isLoading }) {
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onloadend = () => {
      setImageBase64(reader.result);
    };
    reader.readAsDataURL(file);
  };
  
  const togglePlatform = (id) => {
    if (platforms.includes(id)) {
        setPlatforms(platforms.filter(p => p !== id));
    } else {
        setPlatforms([...platforms, id]);
    }
  };

  return (
    <div className="glass-panel">
      <div className="input-group">
        <h2 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <PenTool size={20} color="hsl(var(--accent-primary))" />
          Draft Your Idea
        </h2>
        <p style={{ marginBottom: '1rem', fontSize: '0.9rem' }}>
          Write down your core message. Our AI will automatically rewrite and optimize it for each selected platform.
        </p>
        <textarea
          className="textarea-primary"
          placeholder="e.g., We are so excited to announce the launch of our new AI automation agency next week! We're helping local businesses save 20 hours a week using custom AI workflows..."
          value={baseText}
          onChange={(e) => setBaseText(e.target.value)}
          disabled={isLoading}
          disabled={isLoading}
        ></textarea>
      </div>

      <div className="input-group">
        <label className="input-label" style={{ marginBottom: '0.5rem' }}>Image Upload (Required for Instagram)</label>
        <input
          type="file"
          accept="image/jpeg, image/png, image/webp"
          className="textarea-primary"
          style={{ minHeight: '40px', padding: '0.75rem', cursor: 'pointer' }}
          onChange={handleImageUpload}
          disabled={isLoading}
        />
        {imageBase64 && (
          <div style={{ marginTop: '1rem' }}>
             <img src={imageBase64} alt="Preview" style={{ maxHeight: '150px', borderRadius: '8px', border: '1px solid hsl(var(--border-color))' }}/>
          </div>
        )}
      </div>

      <div className="input-group">
        <label className="input-label" style={{ marginBottom: '0.5rem' }}>Target Platforms</label>
        <div className="platform-grid">
          {platformsList.map(platform => (
            <button
              key={platform.id}
              className={`platform-toggle ${platforms.includes(platform.id) ? 'active' : ''}`}
              onClick={() => togglePlatform(platform.id)}
              disabled={isLoading}
            >
              <div 
                style={{ 
                  width: '12px', 
                  height: '12px', 
                  borderRadius: '50%', 
                  backgroundColor: platforms.includes(platform.id) ? platform.color : 'hsl(var(--text-secondary))'
                }} 
              />
              {platform.name}
            </button>
          ))}
        </div>
      </div>

      <button 
        className="btn-primary" 
        onClick={onGenerate}
        disabled={isLoading || !baseText || platforms.length === 0}
      >
        {isLoading ? (
          <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
            <span className="loader"></span> AI Generating...
          </span>
        ) : (
          <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
            <Send size={18} /> Generate Previews
          </span>
        )}
      </button>
    </div>
  );
}
