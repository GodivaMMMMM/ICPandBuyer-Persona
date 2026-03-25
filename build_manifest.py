import os
import json
import re

base_dir = '/Users/eva.zhang/Desktop/ICPandBuyer Persona'
data_dir = os.path.join(base_dir, 'data')

manifest = []
frontmatter_re = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

for folder in ['icps', 'personas']:
    folder_path = os.path.join(data_dir, folder)
    if not os.path.exists(folder_path):
        continue
    for filename in os.listdir(folder_path):
        if not filename.endswith('.md'):
            continue
        filepath = os.path.join(folder_path, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()
            
        match = frontmatter_re.match(full_content)
        content_body = full_content
        
        meta = {
            'id': f"{folder}/{filename}",
            'title': filename.replace('.md', ''),
            'category': 'ICP' if folder == 'icps' else 'Buyer Persona',
            'tags': [],
            'related': [],
            'content': ''
        }
        
        if match:
            yaml_content = match.group(1)
            content_body = full_content[match.end():]
            for line in yaml_content.split('\n'):
                line = line.strip()
                if line.startswith('title:'):
                    meta['title'] = line.split(':', 1)[1].strip().strip('"').strip("'")
                elif line.startswith('category:'):
                    meta['category'] = line.split(':', 1)[1].strip().strip('"').strip("'")
                elif line.startswith('tags:'):
                    tags_str = line.split(':', 1)[1].strip()
                    if tags_str.startswith('[') and tags_str.endswith(']'):
                        tags = [t.strip().strip('"').strip("'") for t in tags_str[1:-1].split(',')]
                        meta['tags'] = [t for t in tags if t]
                elif line.startswith('related_personas:'):
                    rel_str = line.split(':', 1)[1].strip()
                    if rel_str.startswith('[') and rel_str.endswith(']'):
                        rels = [t.strip().strip('"').strip("'") for t in rel_str[1:-1].split(',')]
                        for r in [x for x in rels if x]:
                            meta['related'].append({'title': r, 'type': 'Buyer Persona'})
                elif line.startswith('related_icps:'):
                    rel_str = line.split(':', 1)[1].strip()
                    if rel_str.startswith('[') and rel_str.endswith(']'):
                        rels = [t.strip().strip('"').strip("'") for t in rel_str[1:-1].split(',')]
                        for r in [x for x in rels if x]:
                            meta['related'].append({'title': r, 'type': 'ICP'})
                        
        meta['content'] = content_body
        manifest.append(meta)

json_data = json.dumps(manifest, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Persona Hub | 客户画像控制台</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; background-color: #f8fafc; color: #0f172a; }
    .glass { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-right: 1px solid #e2e8f0; }
    .prose h1 { font-size: 2rem; font-weight: 700; border-bottom: 2px solid #e2e8f0; padding-bottom: 1rem; margin-bottom: 1.5rem; }
    .prose h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; color: #1e293b; }
    .prose h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; color: #334155; }
    .prose p { margin-bottom: 1rem; }
    .prose ul { list-style-type: disc; padding-left: 1.5rem; margin-bottom: 1.5rem; }
    .prose li { margin-bottom: 0.5rem; }
    .prose strong { color: #0f172a; font-weight: 600; }
    .prose blockquote { border-left: 4px solid #3b82f6; background: #f1f5f9; padding: 1rem 1.5rem; border-radius: 4px; color: #475569; font-style: italic; margin-bottom: 1.5rem; }
    .tag-active { background-color: #3b82f6; color: white; border-color: #3b82f6; }
    .tag-inactive { background-color: white; border-color: #cbd5e1; color: #64748b; }
    .animate-in { animation: fadeIn 0.3s ease-out forwards; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
  </style>
  <script>
    window.PERSONA_DATA = """ + json_data + """;
  </script>
</head>
<body class="h-screen overflow-hidden antialiased">
  <div id="root" class="h-full"></div>

  <script type="text/babel">
    const { useState, useEffect, useMemo, useRef } = React;

    const TAG_DICTIONARY = {
      "基础行业与属相": ["传统制造企业", "出海游戏公司", "AI科技企业", "社交泛娱乐", "中大型企业", "初创型企业"],
      "决策人角色属性": ["核心技术拍板", "成本统筹控制", "稳健型决策者"],
      "架构部署基准": ["强算力基础", "要求混合云架构", "海外多节点覆盖", "网络专线与加速", "极致弹性扩容"],
      "商业痛点与诉求": ["数据与合规优先", "高防抗D刚需", "高并发低延迟", "原厂兜底深度依赖", "免运维托管型", "抵触套路推销", "预算控制严苛"]
    };

    function CreationModal({ isOpen, onClose }) {
      const [text, setText] = useState('');
      const [isDragging, setIsDragging] = useState(false);
      const [copied, setCopied] = useState(false);

      if (!isOpen) return null;

      const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const files = Array.from(e.dataTransfer.files);
        files.forEach(file => {
          if (file.type.startsWith('text/') || file.name.endsWith('.md')) {
            const reader = new FileReader();
            reader.onload = (ev) => {
              setText(prev => prev + `\\n\\n--- Content ---` + ev.target.result + '\\n');
            };
            reader.readAsText(file);
          }
        });
      };

      const handleGeneratePrompt = () => {
        let prompt = `请帮我分析以下客户聊天记录。\\n\\n【分析要求】\\n请调用 \`/analyze-chat\` 逻辑：\\n1. 结构化至 ICP.md 或 Buyer_Persona.md 体系中\\n2. 在 YAML 里打好 Tags！Tags 必须严格、且仅能从以下字典中挑选：\\n`;
        Object.entries(TAG_DICTIONARY).forEach(([group, tags]) => {
            prompt += `- ${group}: ${tags.join(', ')}\\n`;
        });
        prompt += `\\n【输入资料如下】：\\n${text}\\n【请开始提炼！】`;
        
        navigator.clipboard.writeText(prompt).then(() => {
          setCopied(true);
          setTimeout(() => setCopied(false), 3000);
        });
      };

      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm animate-in">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden border">
             <div className="px-6 py-4 flex justify-between items-center bg-slate-50 border-b">
              <h2 className="font-bold">新增画像 (New Insight)</h2>
              <button onClick={onClose}>X</button>
             </div>
             <div className="p-6">
               <textarea className="w-full h-56 p-4 border rounded font-mono text-sm" placeholder="Paste chat logs here..." value={text} onChange={e=>setText(e.target.value)} onDragOver={e=>{e.preventDefault(); setIsDragging(true);}} onDragLeave={()=>setIsDragging(false)} onDrop={handleDrop}></textarea>
             </div>
             <div className="px-6 py-4 bg-slate-50 flex justify-end gap-3">
               <button onClick={onClose} className="px-4 py-2 text-sm">取消</button>
               <button onClick={handleGeneratePrompt} className="px-5 py-2 text-sm bg-blue-600 text-white rounded shadow">{copied ? '已拷贝 Prompt!' : '提取 Prompt'}</button>
             </div>
          </div>
        </div>
      );
    }

    function TagEditorModal({ isOpen, onClose, activeDoc }) {
      const [selectedTags, setSelectedTags] = useState([]);
      const [copied, setCopied] = useState(false);

      useEffect(() => {
        if (isOpen && activeDoc) {
          setSelectedTags([...activeDoc.tags]);
          setCopied(false);
        }
      }, [isOpen, activeDoc]);

      if (!isOpen || !activeDoc) return null;

      const toggleTag = (tag) => {
        setSelectedTags(prev => prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]);
      }

      const handleGenerateTagPrompt = () => {
        const prompt = `请帮我替换文件内容：\\n目标文件：\`${activeDoc.id}\` \\n将里面已有的 tags 整个数组替换为：\\n\`tags: ${JSON.stringify(selectedTags)}\`\\n只修改 tag 这一行，然后运行 build_manifest.py 重新打包！`;
        navigator.clipboard.writeText(prompt).then(() => {
          setCopied(true);
          setTimeout(() => setCopied(false), 3000);
        });
      };

      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-md animate-in">
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-2xl overflow-hidden border">
            <div className="px-6 py-5 border-b flex justify-between items-center bg-slate-50">
              <h2 className="font-bold">为「{activeDoc.title}」配置标签</h2>
              <button onClick={onClose}>X</button>
            </div>
            <div className="px-6 py-4 max-h-[60vh] overflow-y-auto">
              <p className="text-sm text-slate-500 bg-blue-50 p-3 rounded-xl mb-6">点击全局字典标签进行开关。选好后生成指令给 AI。</p>
              <div className="flex flex-col gap-6">
                {Object.entries(TAG_DICTIONARY).map(([groupName, tags]) => (
                  <div key={groupName}>
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3 border-b">{groupName}</h3>
                    <div className="flex flex-wrap gap-2">
                       {tags.map(tag => (
                          <button key={tag} onClick={() => toggleTag(tag)} className={`px-3 py-1.5 rounded-lg text-sm border ${selectedTags.includes(tag) ? 'bg-blue-600 text-white border-blue-600' : 'bg-slate-50 text-slate-600'}`}>
                            {tag}
                          </button>
                       ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="px-6 py-4 flex justify-end gap-3 bg-slate-50 border-t">
              <button onClick={onClose} className="px-4 py-2 text-sm">取消</button>
              <button onClick={handleGenerateTagPrompt} className="px-5 py-2 text-sm bg-slate-800 text-white rounded flex items-center">{copied ? '已拷贝！请去粘贴' : '生成修改指令'}</button>
            </div>
          </div>
        </div>
      );
    }
    
    function ReportModal({ isOpen, onClose, filteredDocs, activeTag }) {
      const [selectedIds, setSelectedIds] = useState([]);
      const [copied, setCopied] = useState(false);
      const [articleTopic, setArticleTopic] = useState('');

      useEffect(() => {
        if (isOpen) {
          setSelectedIds(filteredDocs.map(d => d.id));
          setCopied(false);
        }
      }, [isOpen, filteredDocs]);

      if (!isOpen) return null;

      const toggleDoc = (id) => {
        setSelectedIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);
      };

      const handleGenerateReportPrompt = () => {
        const selectedDocs = filteredDocs.filter(d => selectedIds.includes(d.id));
        if (selectedDocs.length === 0) return;

        let prompt = `我为你整理了以下精心收集的理想客户画像（ICP）和关键买家角色（Buyer Persona）组合样本数据（共 ${selectedDocs.length} 份）。\\n\\n`;
        prompt += `【分析任务】\\n请你作为资深用户分析师，深入分析这些在局部的独立数据，提炼他们之间的相互逻辑联系、整体痛点共性、核心诉求特征，将它们有机糅合在一起，输出一份客观、详实的【客观群像特征档案 (Objective Group Profile)】。\\n`;
        if (articleTopic) {
            prompt += `特别关注焦点：在总结时，请着重挖掘与【${articleTopic}】相关的共性。\\n`;
        }
        prompt += `\\n【输出要求】\\n这应当是一份无需包含具体的销售或营销目的的“纯底层分析底稿”。请梳理得条理清晰，呈现出该群体最真实客观的全景面貌。\\n\\n`;
        prompt += `========================= 以下是提交的样本数据 =========================\\n\\n`;
        selectedDocs.forEach((doc, idx) => {
            prompt += `--- 第 ${idx+1} 个画像样本：[${doc.category}] ${doc.title} ---\\n`;
            prompt += `${doc.content}\\n\\n`;
        });
        prompt += `========================= 样本数据结束 =========================\\n\\n`;
        prompt += `【请立刻开始提炼并输出这篇中立的群像底层档案！】`;

        navigator.clipboard.writeText(prompt).then(() => {
          setCopied(true);
          setTimeout(() => setCopied(false), 4000);
        });
      };

      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-3xl flex flex-col max-h-[90vh] overflow-hidden">
            <div className="px-6 py-4 flex justify-between items-center bg-slate-50 border-b shrink-0">
              <h2 className="font-bold">群像洞察生成器</h2>
              <button onClick={onClose}>X</button>
            </div>
            <div className="p-6 overflow-y-auto flex-1 bg-slate-50/30">
              <input type="text" placeholder="可选: 特定关注主题" className="w-full px-4 py-2 border rounded-lg mb-4 text-sm" value={articleTopic} onChange={e=>setArticleTopic(e.target.value)} />
              <div className="grid grid-cols-2 gap-3">
                {filteredDocs.map(doc => (
                  <label key={doc.id} className="flex items-start gap-3 p-3 rounded-xl border bg-white cursor-pointer">
                    <input type="checkbox" checked={selectedIds.includes(doc.id)} onChange={() => toggleDoc(doc.id)} />
                    <div className="flex-1 min-w-0">
                      <div className="font-semibold text-sm line-clamp-1">{doc.title}</div>
                      <div className="text-xs text-slate-500">{doc.category}</div>
                    </div>
                  </label>
                ))}
              </div>
            </div>
            <div className="px-6 py-4 flex justify-end gap-3 bg-slate-50 border-t">
              <button onClick={onClose} className="px-4 py-2 text-sm">取消</button>
              <button onClick={handleGenerateReportPrompt} className="px-5 py-2 text-sm bg-slate-800 text-white rounded">{copied?'已拷贝 Prompt':'打包成群像 Prompt'}</button>
            </div>
          </div>
        </div>
      );
    }

    function App() {
      const [manifest, setManifest] = useState(window.PERSONA_DATA || []);
      const [activeDoc, setActiveDoc] = useState(manifest.length > 0 ? manifest[0] : null);
      const [activeTag, setActiveTag] = useState(null);
      const [search, setSearch] = useState('');
      
      const [isCreateModalOpen, setCreateModalOpen] = useState(false);
      const [isReportModalOpen, setReportModalOpen] = useState(false);
      const [isTagModalOpen, setTagModalOpen] = useState(false);

      const filteredDocs = manifest.filter(doc => {
        const matchTag = activeTag ? doc.tags.includes(activeTag) : true;
        const matchSearch = doc.title.toLowerCase().includes(search.toLowerCase());
        return matchTag && matchSearch;
      });

      const handleJumpToRelated = (relatedTitle) => {
        const target = manifest.find(d => d.title === relatedTitle);
        if (target) {
          setActiveDoc(target);
          setActiveTag(null);
          setSearch('');
        }
      };

      return (
        <div className="flex h-full">
          {/* Sidebar */}
          <div className="w-[340px] glass flex flex-col h-full shadow-lg z-10 shrink-0">
            <div className="p-5 border-b border-slate-200">
              <h1 className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-800 mb-5">Persona Hub</h1>
              <div className="flex gap-2 mb-4">
                <button onClick={() => setCreateModalOpen(true)} className="flex-1 bg-blue-600 text-white py-2 rounded-xl text-xs font-semibold shadow">新建画像</button>
                <button onClick={() => setReportModalOpen(true)} className="flex-1 bg-slate-800 text-white py-2 rounded-xl text-xs font-semibold shadow">导群像报告</button>
              </div>
              <input type="text" placeholder="检索画像..." className="w-full px-4 py-2 rounded-lg border text-sm" value={search} onChange={e => setSearch(e.target.value)} />
            </div>
            
            <div className="p-5 flex-1 overflow-y-auto">
              <div className="mb-8">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-xs font-bold text-slate-400">标签分类 (TAG DICTIONARY)</h3>
                  {activeTag && <button onClick={()=>setActiveTag(null)} className="text-[10px] text-blue-600">清除</button>}
                </div>
                <div className="flex flex-col gap-4">
                  {Object.entries(TAG_DICTIONARY).map(([groupName, tags]) => (
                    <div key={groupName}>
                      <h4 className="text-[10px] font-bold text-slate-300 mb-1.5">{groupName}</h4>
                      <div className="flex flex-wrap gap-1.5">
                        {tags.map(tag => {
                          const hasDocs = manifest.some(d => d.tags.includes(tag));
                          if (!hasDocs && activeTag !== tag) return null;
                          return (
                            <button 
                              key={tag} onClick={() => setActiveTag(tag === activeTag ? null : tag)}
                              className={`px-2 py-1.5 rounded-md text-[11px] font-semibold border transition-all ${activeTag === tag ? 'bg-blue-600 text-white border-blue-600 shadow' : 'bg-white text-slate-600 border-slate-200 shadow-sm hover:border-blue-400'}`}
                            >{tag}</button>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-xs font-bold text-slate-400 mb-3">画像文档 ({filteredDocs.length})</h3>
                <div className="flex flex-col gap-2">
                  {filteredDocs.map(doc => (
                     <div key={doc.id} onClick={() => setActiveDoc(doc)} className={`p-3 rounded-xl border cursor-pointer ${activeDoc?.id === doc.id ? 'border-blue-500 bg-white shadowring-1 ring-blue-500' : 'bg-white border-slate-200'}`}>
                      <div className="font-semibold text-sm mb-1 line-clamp-1">{doc.title}</div>
                      <div className="text-xs text-slate-500">{doc.category} · {doc.tags.length} 标签</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Main Area */}
          <div className="flex-1 bg-slate-50 overflow-y-auto p-10 flex gap-8 items-start relative justify-center">
            {activeDoc ? (
              <>
                <div className="bg-white max-w-3xl w-full rounded-2xl shadow-sm border p-12 shrink-0">
                  <span className="px-3 py-1 bg-slate-100 rounded-lg text-xs font-bold">{activeDoc.category}</span>
                  <h1 className="text-3xl font-bold mt-4 mb-8 pb-6 border-b">{activeDoc.title}</h1>
                  <div className="prose prose-slate max-w-none" dangerouslySetInnerHTML={{__html: marked.parse(activeDoc.content)}}></div>
                </div>

                <div className="w-80 shrink-0 sticky top-10 flex flex-col gap-5 pt-2">
                  {activeDoc.related.length > 0 && (
                    <div className="bg-white rounded-2xl border p-6 shadow-sm">
                      <h4 className="text-xs font-bold text-slate-400 mb-4">关联画像 (Related)</h4>
                      <div className="flex flex-col gap-2">
                        {activeDoc.related.map(rel => (
                          <button key={rel.title} onClick={() => handleJumpToRelated(rel.title)} className="p-3 bg-slate-50 border rounded-xl text-sm font-semibold text-left hover:border-blue-400">
                             {rel.title}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="bg-white rounded-2xl border p-6 shadow-sm group relative">
                    <div className="flex justify-between items-center mb-4">
                      <h4 className="text-xs font-bold text-slate-400">特征矩阵 (Tags)</h4>
                      <button onClick={(e) => { e.stopPropagation(); setTagModalOpen(true); }} className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity">✏️ 编辑</button>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {activeDoc.tags.map(tag => (
                        <span key={tag} onClick={() => setActiveTag(tag)} className="px-3 py-1.5 bg-blue-50 text-blue-700 border border-blue-200 rounded-lg text-xs font-semibold">{tag}</span>
                      ))}
                    </div>
                  </div>
                </div>
              </>
            ) : null}
          </div>

          <CreationModal isOpen={isCreateModalOpen} onClose={() => setCreateModalOpen(false)} />
          <ReportModal isOpen={isReportModalOpen} onClose={() => setReportModalOpen(false)} filteredDocs={filteredDocs} activeTag={activeTag} />
          <TagEditorModal isOpen={isTagModalOpen} onClose={() => setTagModalOpen(false)} activeDoc={activeDoc} />
        </div>
      );
    }

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
"""

with open(os.path.join(base_dir, 'dashboard.html'), 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Dashboard with Split UI, standard dictionary, and Tag Manager built successfully!")
