import React, { useState, useEffect, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import fm from 'front-matter';
import { LayoutDashboard, FileText, UserCircle, Tag as TagIcon, Search } from 'lucide-react';

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [activeDoc, setActiveDoc] = useState(null);
  const [activeTag, setActiveTag] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  // Load all markdown files from the data directory
  useEffect(() => {
    // Vite specific: import.meta.glob with eager: true loads the text at build/dev time
    const mdFiles = import.meta.glob('../../data/**/*.md', { as: 'raw', eager: true });
    
    const parsedDocs = Object.keys(mdFiles).map((path) => {
      const rawContent = mdFiles[path];
      const parsed = fm(rawContent);
      
      // Determine type from path logic
      let type = 'Unknown';
      if (path.includes('/icps/')) type = 'ICP';
      if (path.includes('/personas/')) type = 'Persona';

      return {
        id: path,
        title: parsed.attributes.title || path.split('/').pop().replace('.md', ''),
        category: parsed.attributes.category || type,
        tags: parsed.attributes.tags || [],
        date: parsed.attributes.date || new Date().toISOString().split('T')[0],
        content: parsed.body,
        rawFrontmatter: parsed.attributes
      };
    });

    setDocuments(parsedDocs);
    if (parsedDocs.length > 0) setActiveDoc(parsedDocs[0]);
  }, []);

  // Compute all unique tags
  const allTags = useMemo(() => {
    const tags = new Set();
    documents.forEach(doc => {
      doc.tags.forEach(tag => tags.add(tag));
    });
    return Array.from(tags).sort();
  }, [documents]);

  // Filter documents
  const filteredDocs = useMemo(() => {
    return documents.filter(doc => {
      const matchesTag = activeTag ? doc.tags.includes(activeTag) : true;
      const matchesSearch = doc.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            doc.content.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesTag && matchesSearch;
    });
  }, [documents, activeTag, searchQuery]);

  return (
    <div className="app-container">
      {/* Sidebar Area */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <LayoutDashboard size={20} />
          </div>
          Persona Hub
        </div>

        <div style={{ position: 'relative', marginBottom: '1.5rem' }}>
          <Search size={16} color="var(--text-secondary)" style={{ position: 'absolute', left: '12px', top: '10px' }} />
          <input 
            type="text" 
            placeholder="Search documents..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ 
              width: '100%', padding: '0.5rem 1rem 0.5rem 2.25rem', 
              borderRadius: '8px', border: '1px solid var(--border)', outline: 'none',
              fontFamily: 'inherit', fontSize: '0.85rem'
            }}
          />
        </div>

        <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '0.75rem', letterSpacing: '0.05em' }}>
          Filters ({allTags.length} Tags)
        </h3>
        <div className="tag-list">
          <span 
            className={`tag ${activeTag === null ? 'active' : ''}`}
            onClick={() => setActiveTag(null)}
          >
            All
          </span>
          {allTags.map(tag => (
            <span 
              key={tag} 
              className={`tag ${activeTag === tag ? 'active' : ''}`}
              onClick={() => setActiveTag(tag === activeTag ? null : tag)}
            >
              #{tag}
            </span>
          ))}
        </div>

        <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '0.75rem', letterSpacing: '0.05em' }}>
          Documents ({filteredDocs.length})
        </h3>
        <div className="file-list">
          {filteredDocs.map(doc => (
            <div 
              key={doc.id} 
              className={`file-item ${activeDoc?.id === doc.id ? 'active' : ''}`}
              onClick={() => setActiveDoc(doc)}
            >
              <div className="file-title" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                {doc.category === 'ICP' ? <FileText size={16} color="var(--accent)"/> : <UserCircle size={16} color="var(--accent)"/>}
                {doc.title}
              </div>
              <div className="file-meta">
                <span>{doc.category}</span>
                <span>{doc.tags.length} Tags</span>
              </div>
            </div>
          ))}
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {activeDoc ? (
          <div className="markdown-container">
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '2rem', flexWrap: 'wrap' }}>
              {activeDoc.tags.map(tag => (
                   <span key={tag} style={{ background: '#f1f5f9', color: '#475569', fontSize: '0.75rem', padding: '4px 8px', borderRadius: '4px', fontWeight: 500, display: 'flex', alignItems: 'center', gap: '4px'}}>
                      <TagIcon size={12}/> {tag}
                   </span>
              ))}
            </div>
            <div className="prose">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {activeDoc.content}
              </ReactMarkdown>
            </div>
          </div>
        ) : (
          <div className="empty-state">
            <LayoutDashboard size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
            <h3>No Document Selected</h3>
            <p>Select a persona or ICP from the sidebar to view details.</p>
          </div>
        )}
      </main>
    </div>
  );
}
