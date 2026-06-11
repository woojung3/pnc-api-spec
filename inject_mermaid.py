import os
import sys

target = "dist/index.html"
if not os.path.exists(target):
    print(f"Error: {target} not found")
    sys.exit(1)

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

# [SUPER STABLE] Mermaid Orchestration for Redocly
mermaid_script = """
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({
    startOnLoad: false,
    theme: 'neutral',
    securityLevel: 'loose',
    logLevel: 'error'
  });

  let isRendering = false;
  const renderQueue = [];

  async function processQueue() {
    if (isRendering || renderQueue.length === 0) return;
    isRendering = true;

    while (renderQueue.length > 0) {
      const { el, idx } = renderQueue.shift();
      const pre = el.parentElement;
      const source = el.textContent;
      const chartId = `mermaid-svg-${Date.now()}-${idx}`;

      try {
        // 1. 컨테이너 생성 및 스타일 강제 고정
        const wrapper = document.createElement('div');
        wrapper.style.cssText = "display: block !important; width: 100% !important; clear: both !important; margin: 30px 0 !important; padding: 10px !important; background: white !important; border: 1px solid #eee !important; min-height: 100px; position: relative !important;";
        
        const chartDiv = document.createElement('div');
        chartDiv.id = chartId;
        wrapper.appendChild(chartDiv);

        // 2. React DOM 깨지지 않게 pre 앞에 삽입 후 pre 숨김
        pre.parentNode.insertBefore(wrapper, pre);
        pre.style.display = 'none';

        // 3. 비동기 렌더링 (await 사용하여 순차 처리 보장)
        const { svg } = await mermaid.render(chartId + "-svg", source);
        chartDiv.innerHTML = svg;
        
        // 4. SVG 크기 강제 보정
        const svgEl = chartDiv.querySelector('svg');
        if (svgEl) {
          svgEl.style.maxWidth = "100%";
          svgEl.style.height = "auto";
        }
      } catch (e) {
        console.error("Mermaid Render Error:", e);
        pre.style.display = 'block';
      }
      // 다음 차트 렌더링 전 브라우저에게 숨 돌릴 틈을 줌
      await new Promise(resolve => setTimeout(resolve, 50));
    }
    isRendering = false;
  }

  function scanAndQueue() {
    const codes = document.querySelectorAll('pre code.language-mermaid');
    let added = false;
    codes.forEach((el, idx) => {
      if (el.dataset.processed) return;
      el.dataset.processed = 'true';
      renderQueue.push({ el, idx });
      added = true;
    });
    if (added) processQueue();
  }

  // Redocly의 렌더링 사이클에 맞춰 감시
  const observer = new MutationObserver(() => scanAndQueue());
  observer.observe(document.body, { childList: true, subtree: true });
  
  // 초기 실행 및 주기적 보정
  scanAndQueue();
  setInterval(scanAndQueue, 1500);
</script>
"""

if "mermaid.min.js" not in content:
    new_content = content.replace("</body>", mermaid_script + "</body>")
    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Super-stable Mermaid injected.")
else:
    # 기존 스크립트가 있으면 교체
    import re
    new_content = re.sub(r'<script src="https://cdn.jsdelivr.net/npm/mermaid.*?</script>', mermaid_script, content, flags=re.DOTALL)
    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Mermaid script updated to super-stable version.")
