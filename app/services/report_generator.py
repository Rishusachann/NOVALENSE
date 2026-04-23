from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from jinja2 import Template
from app.core.config import settings

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>NOVALENSE Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 32px; color: #222; }
    h1, h2 { color: #0d47a1; }
    .card { border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin-bottom: 16px; }
    .score { font-size: 28px; font-weight: bold; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #f2f5fb; }
  </style>
</head>
<body>
  <h1>NOVALENSE Analysis Report</h1>
  <div class="card">
    <p><strong>Document:</strong> {{ document_name }}</p>
    <p class="score">Originality Score: {{ originality_score }}</p>
    <p><strong>Semantic Similarity:</strong> {{ module_scores.semantic_similarity_score }}</p>
    <p><strong>Paraphrase Score:</strong> {{ module_scores.paraphrase_score }}</p>
    <p><strong>AI Likelihood:</strong> {{ module_scores.ai_likelihood_score }}</p>
  </div>

  <h2>Top Similar Papers</h2>
  <table>
    <tr><th>Title</th><th>Year</th><th>Score</th><th>Source</th></tr>
    {% for item in top_similar_papers %}
    <tr>
      <td>{{ item.title }}</td>
      <td>{{ item.year }}</td>
      <td>{{ item.score }}</td>
      <td>{{ item.source }}</td>
    </tr>
    {% endfor %}
  </table>

  <h2>Flagged Sentences</h2>
  {% for item in flagged_sentences %}
  <div class="card">
    <p><strong>Input:</strong> {{ item.input_sentence }}</p>
    <p><strong>Matched:</strong> {{ item.matched_sentence }}</p>
    <p><strong>Matched Paper:</strong> {{ item.matched_paper_title }}</p>
    <p><strong>Similarity:</strong> {{ item.similarity }} | <strong>Paraphrase:</strong> {{ item.paraphrase_probability }}</p>
    <p><strong>Explanation:</strong> {{ item.explanation }}</p>
  </div>
  {% endfor %}

  <h2>AI Detection Explanations</h2>
  <ul>
    {% for note in ai_explanations %}
    <li>{{ note }}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""


def save_report(payload: dict) -> tuple[str, str]:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = Path(payload["document_name"]).stem
    json_path = settings.reports_dir / f"{stem}_{timestamp}.json"
    html_path = settings.reports_dir / f"{stem}_{timestamp}.html"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    html = Template(HTML_TEMPLATE).render(**payload)
    html_path.write_text(html, encoding="utf-8")
    return str(json_path), str(html_path)
