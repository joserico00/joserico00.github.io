"""Generate the portfolio from editable project data and the home template."""
from pathlib import Path
from html import escape as e
import json,re

SITE=Path(__file__).resolve().parents[1]
PROJECTS=json.loads((SITE/'data/projects.json').read_text(encoding='utf-8'))
BY_SLUG={p['slug']:p for p in PROJECTS}
THEMES={
 'ai-hpc':('AI & HPC','Transformers, computing systems, and scientific simulations.'),
 'security':('Cybersecurity','Network defense, traffic analysis, and security education.'),
 'research':('Research software','Tools and reproducible workflows for scientific questions.'),
 'software':('Software & community','Applications, automation, and tools for everyday work.'),
 'data':('Data & analysis','From raw records to useful datasets, reports, and figures.'),
 'systems':('Systems & foundations','Distributed storage, operating systems, and coursework.'),
 'teaching':('Teaching & outreach','Learning through notebooks, workshops, and challenges.'),
}
CV='downloads/Jose_Rodriguez_Rios_CV_2026-09.pdf'
RESUME='downloads/Jose_Rodriguez_Rios_General_Resume_2026-09.pdf'

def nav(prefix='',active=''):
    links=[('projects.html','Projects'),('experience.html','Experience'),('awards.html','Awards'),('workshops.html','Workshops')]
    return f'''<header class="site-header wrap"><a class="wordmark" href="{prefix or './'}" aria-label="José Rodríguez-Ríos home">JR<span class="mark-period">.</span></a><button class="menu-toggle" type="button" aria-controls="main-navigation" aria-expanded="false" hidden>Menu <span aria-hidden="true">+</span></button><nav id="main-navigation" aria-label="Main navigation">{''.join(f'<a href="{prefix}{url}"'+(' aria-current="page"' if active==url else '')+f'>{label}</a>' for url,label in links)}<a href="{prefix}{RESUME}" download>Resume ↓</a><a class="nav-cv" href="{prefix}{CV}" download>CV ↓</a></nav></header>'''

def footer(prefix=''):
    return f'''<footer class="wrap footer"><span>© 2026 José E. Rodríguez-Ríos</span><div><a href="{prefix or './'}">Home</a><a href="{prefix}projects.html">Projects</a><a href="mailto:jerr.ccom@gmail.com">Contact</a><a href="https://github.com/joserico00">GitHub ↗</a></div><a href="#main">Back to top ↑</a></footer>'''

def page(title,description,body,prefix='',active=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{e(description)}"><meta name="theme-color" content="#102a43"><title>{e(title)} · José E. Rodríguez-Ríos</title><link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg"><link rel="stylesheet" href="{prefix}styles.css"><script src="{prefix}site.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a>{nav(prefix,active)}<main id="main">{body}</main>{footer(prefix)}</body></html>'''

def intro(number,title,description):
    return f'<section class="wrap page-intro"><p class="eyebrow">{number} / EXPLORE</p><h1>{title}</h1><p>{description}</p></section>'

def tags(p): return '<div class="tags">'+''.join(f'<span>{e(t)}</span>' for t in p['tags'])+'</div>'

def project_card(p):
    link=f'<a href="{p["github"]}">GitHub <span aria-hidden="true">↗</span><span class="sr-only"> for {e(p["title"])}</span></a>' if p['github'] else '<span class="resource-note">National laboratory experience</span>'
    return f'''<article class="catalog-card" data-themes="{' '.join(p['themes'])}" data-project="{p['slug']}"><p class="eyebrow">{e(p['category'])}</p><h2><a href="projects/{p['slug']}.html">{e(p['title'])}</a></h2><p class="project-context">{e(p['context'])}</p><p class="catalog-summary">{e(p['summary'])}</p>{tags(p)}<div class="card-links"><a href="projects/{p['slug']}.html">Read project <span aria-hidden="true">↗</span><span class="sr-only">: {e(p['title'])}</span></a>{link}</div></article>'''

def build_catalog():
    buttons='<button type="button" data-theme="all" aria-pressed="true">All projects <span>18</span></button>'
    buttons+=''.join(f'<button type="button" data-theme="{k}" aria-pressed="false">{label} <span>{sum(k in p["themes"] for p in PROJECTS)}</span></button>' for k,(label,_) in THEMES.items())
    body=intro('01','Projects, connected by theme.','Explore work in scientific computing, cybersecurity, community software, and the foundations behind it. Some projects belong to more than one theme.')
    body+=f'''<section class="wrap catalog-section" aria-label="Project collection"><div class="project-filters" aria-label="Filter projects by theme" hidden>{buttons}</div><div class="catalog-status"><p id="project-count" role="status" aria-live="polite" aria-atomic="true">Showing all 18 projects</p><a href="./#work">See the four featured projects ↑</a></div><div class="catalog-grid">{''.join(project_card(p) for p in PROJECTS)}</div><p id="no-projects" hidden>No projects match this theme. Choose another theme above.</p><noscript><p>All projects are shown. Each card links to its project page and public source where available.</p></noscript></section>'''
    (SITE/'projects.html').write_text(page('Projects','Browse 18 projects by theme, with case studies and verified GitHub links.',body,active='projects.html'),encoding='utf-8')

def build_cases():
    for p in PROJECTS:
        content=p.get('body_html') or f'<h2>The project</h2><p>{e(p["summary"])}</p><h2>Implementation and context</h2><p>{e(p["details"])}</p>'
        if p['slug']=='traffic-detection':
            content+='<div class="result"><strong>Evaluation without capture overlap</strong><p>The current pipeline keeps capture IDs disjoint and fits preprocessing only on training data. The repository documents historical results and their limitations; it does not claim a new benchmark score for this revision.</p></div>'
        if p['slug']=='fusion-energy':
            content+='<div class="result"><strong>4.8 MW of a 12 MW facility budget</strong><p>The scheduler’s constraint is the fusion-workload allocation, while the mentoring project considered the broader facility budget.</p></div>'
        meta=''.join(f'<div><span>{label}</span><p>{e(p[key])}</p></div>' for key,label in [('role','MY ROLE'),('org','ORGANIZATION'),('date','WHEN')] if p.get(key))
        github=f'<a href="{p["github"]}" class="button primary">View on GitHub ↗</a>' if p['github'] else ''
        resources=f'<a href="{p["github"]}">Source code and documentation ↗</a>' if p['github'] else '<p>This case study describes my internship contributions. No public repository is linked.</p>'
        if p['slug']=='nvsrco': resources+='<a href="https://repositorio.upr.edu/handle/11721/4342">Graduate technical report ↗</a>'
        theme_links=''.join(f'<a class="theme-link" href="../projects.html?theme={k}">{THEMES[k][0]}</a>' for k in p['themes'])
        related=[x for x in PROJECTS if x['slug']!=p['slug'] and set(x['themes'])&set(p['themes'])][:3]
        body=f'''<section class="case-hero wrap"><a class="back-link" href="../projects.html">← All projects</a><p class="eyebrow">{e(p['category'])}</p><h1>{e(p['title'])}</h1><p class="case-deck">{e(p['summary'])}</p><p class="project-context">{e(p['context'])}</p><div class="case-meta">{meta}</div>{github}</section><div class="case-layout wrap"><article class="case-copy">{content}</article><aside class="case-sidebar" aria-label="Project resources"><h2>Tools &amp; technologies</h2>{tags(p)}<h2>Explore further</h2>{resources}<a href="../{CV}" download>Download full CV (PDF) ↓</a><h2>Related themes</h2>{theme_links}</aside></div><section class="related-projects wrap"><p class="eyebrow">KEEP EXPLORING</p><h2>Related work</h2><div class="related-grid">{''.join(f'<a href="{x["slug"]}.html"><span>{e(x["category"])}</span>{e(x["title"])} ↗</a>' for x in related)}</div></section>'''
        (SITE/'projects'/f'{p["slug"]}.html').write_text(page(p['title'],p['summary'],body,'../'),encoding='utf-8')

def record(date,title,org,text,links=()):
    return f'''<article class="detail-record"><div class="record-date">{e(date)}</div><div><h2>{title}</h2><p class="record-org">{org}</p><p>{text}</p><div class="record-links">{''.join(f'<a class="text-link" href="{url}">{label} ↗</a>' for label,url in links)}</div></div></article>'''

def build_experience():
    body=intro('02','Experience','Research, engineering, and teaching across national laboratories, the University of Puerto Rico, and my community.')
    rows=[
      ('JUN – AUG 2026','Research Intern','Argonne National Laboratory · Lemont, IL','Developed regulatory-genomics learning workflows on Perlmutter, Polaris, and Aurora. Led a 10-student bootcamp project, created notebook and SLURM lessons, and wrote resources for future project leads. Also developed ALCF Compute Finder to help users choose computing systems.', [('Genomics project','projects/genomics.html'),('Compute Finder','projects/compute-finder.html')]),
      ('2024 – PRESENT','Volunteer Software Developer','Cooperativa de Energía La Margarita (Abeyno Coop) · Salinas, PR','Built Solar Fleet Reporter to collect solar-fleet energy data, apply net-metering billing rules, and produce monthly reports and homeowner statements.', [('Solar Fleet Reporter','projects/solar-fleet.html')]),
      ('AUG 2022 – MAY 2025','Graduate Research &amp; Teaching Assistant','UPR Río Piedras · Laboratory of Dr. José Ortiz Ubarri and Department of Computer Science','Designed NVSRCO for resource-constrained organizations. Led Operating Systems, Computer Architecture, and Cybersecurity labs, and created CTF challenges and outreach activities for about 60 high-school students.', [('NVSRCO','projects/nvsrco.html'),('CTF challenges','projects/ctf-challenges.html')]),
      ('JUN – AUG 2024','DevOps Intern','Lawrence Livermore National Laboratory · Livermore, CA','Containerized cyber-research applications and integrated GitLab CI/CD. Built an Elasticsearch store for Ghidra BSim features and deployed a Docker-hosted Ollama Llama 3 service for PaperQA.', [('Research infrastructure','projects/research-infrastructure.html')]),
      ('JUN – AUG 2022','Cybersecurity Intern','GM Sectech · San Juan, PR','Supported penetration-testing scenarios involving credentials, password cracking, and domain compromise. Developed a Python/Twilio SMS phishing simulator for controlled security-awareness training.', []),
      ('2020','Undergraduate Research Assistant','UPR Río Piedras · Laboratory of Dr. José Ortiz Ubarri','Developed a decoy university website using honeypot techniques to study automated attack activity and its origins.', []),
      ('2019','Undergraduate Software Assistant','UPR Río Piedras · Molecular Biology Laboratory of Dr. José A. Rodríguez-Martínez','Maintained and extended NRLB, a Java tool for protein–DNA interaction analysis. Adapted analysis code for DNA-binding sequences and supported laboratory researchers under NIH grant SC1GM127231.', []),
    ]
    body+='<section class="wrap records-section" aria-label="Professional and research experience">'+''.join(record(*row) for row in rows)+'</section>'
    body+='<section class="about-section"><div class="wrap section"><p class="eyebrow">EDUCATION</p><div class="education-grid"><article><span>2026 – PRESENT</span><h2>Ph.D. in Software Engineering</h2><p>University of Puerto Rico · Mayagüez</p></article><article><span>2022 – 2025</span><h2>M.S. in Computer Science</h2><p>University of Puerto Rico · Río Piedras<br>GPA: 4.0 / 4.0</p></article><article><span>2015 – 2020</span><h2>B.S. in Computer Science</h2><p>University of Puerto Rico · Río Piedras<br>Minor in Cybersecurity</p></article></div></div></section>'
    body+=f'<div class="wrap page-downloads"><a class="button primary" href="{RESUME}" download>Download Resume ↓</a><a class="text-link" href="{CV}" download>Download full CV ↓</a><a class="text-link" href="workshops.html">Teaching and workshops ↗</a></div>'
    (SITE/'experience.html').write_text(page('Experience','National laboratory, research, community software, and teaching experience.',body,active='experience.html'),encoding='utf-8')

def build_awards():
    body=intro('03','Awards &amp; recognition','Team competitions, selective programs, and support for my studies and research.')
    rows=[
      ('APRIL 2024','1st place · 30 teams','BSides Puerto Rico Capture the Flag · San Juan, PR','Competed as part of a three-member team, solving reverse-engineering, cryptography, network-analysis, and binary-exploitation challenges.', [('Explore security projects','projects.html?theme=security')]),
      ('APRIL 2024','Selected from 400+ applicants','Bloomberg HSI Tech Summit · New York, NY','One of 29 students selected for live coding and engineering sessions. Subsequently invited to the six-week Bloomberg Summer Accelerator.', []),
      ('SEPTEMBER 2022','5th place','Bloomberg Hackathon · UPR Río Piedras','Built Seniory, a Python desktop application connecting older adults with nearby caregivers or volunteers through location-based help requests.', [('Seniory project','projects/seniory.html')]),
      ('DECEMBER 2019','2nd place team','Tracer Fire Blue Team Competition · ACSAC','Worked on incident investigation, disk and memory forensics, malware analysis, and binary reversing in a competition with 40 participants.', []),
    ]
    body+='<section class="wrap records-section" aria-label="Awards">'+''.join(record(*row) for row in rows)+'</section>'
    body+='<section class="about-section"><div class="wrap section"><p class="eyebrow">SCHOLARSHIPS &amp; RESEARCH SUPPORT</p><div class="extra-grid"><article><h3>Francis Castro Scholarship</h3><p>University of Puerto Rico<br>2020 and 2022</p></article><article><h3>PR-LSAMP Undergraduate Fellow</h3><p>Puerto Rico Louis Stokes Alliance for Minority Participation<br>2020</p></article><article><h3>Research supported by NIH</h3><p>Software support in the Rodríguez-Martínez laboratory under grant SC1GM127231.<br>2019</p></article></div></div></section>'
    (SITE/'awards.html').write_text(page('Awards','Competitions, honors, scholarships, and research support.',body,active='awards.html'),encoding='utf-8')

def build_workshops():
    body=intro('04','Workshops &amp; outreach','From discovering high-performance computing to helping others take their first steps.')
    body+='<section class="wrap learning-path" aria-label="HPC bootcamp progression"><div><span>2023</span><strong>Participant</strong><p>Heatwaves and power outages</p></div><span aria-hidden="true">→</span><div><span>2025</span><strong>Peer mentor</strong><p>Fusion workloads and energy</p></div><span aria-hidden="true">→</span><div><span>2026</span><strong>Project lead</strong><p>Transformers and regulatory DNA</p></div></section>'
    rows=[
      ('2026','Genomics on HPC · Project Lead','Intro to HPC Bootcamp · Argonne National Laboratory','Scoped a 10–12-hour project and led 10 students in two sub-teams through DNA tokenization, model training, HPC job submission, and final presentations. Created guides and reusable notebook templates for future project leads.', [('Genomics curriculum','projects/genomics.html')]),
      ('2026','Epidemic modeling teaching notebooks','Intro to HPC learning materials','Developed complementary learning tracks for deterministic SIR models and stochastic simulations, with a master notebook, reproducible examples, and browser-readable notebook previews.', [('Epidemic modeling','projects/epidemic-modeling.html')]),
      ('2026','Human neural network activity','Argonne 80th Anniversary Open House','Volunteered in a hands-on activity where visitors passed an image description through a human “neural network.” Built a small LLM-assisted app to let a single visitor participate when the full group was not available.', []),
      ('AUGUST 2025','Fusion workloads · Peer Mentor','Intro to HPC Bootcamp · Argonne program','One of two peer mentors supporting a 10-student project; directly mentored five students. Helped participants use Python and data analysis to investigate HPC energy trade-offs under a 12 MW facility budget. My scheduler notebooks allocate 4.8 MW of that budget to fusion workloads.', [('Fusion energy notebooks','projects/fusion-energy.html')]),
      ('2023 – 2025','CTF workshops &amp; school outreach','University of Puerto Rico · Río Piedras','Created progressively more challenging exercises in cryptography, forensics, Linux, scripting, and related security topics. Ran coding and outreach activities for about 60 Puerto Rico high-school students.', [('Workshop challenges','projects/ctf-challenges.html')]),
      ('2023','Power outages &amp; heatwaves · Participant','Intro to HPC Bootcamp · Berkeley Lab / NERSC','Used Python, pandas, and Matplotlib on Perlmutter with a team studying the June 2016 Southwest heatwave, power outages, and populations relying on electricity-dependent medical equipment. Presented the findings in a lightning talk.', [('Power-outage analysis','projects/power-outages.html')]),
      ('2024','HSI Tech Summit &amp; Summer Accelerator','Bloomberg','Selected for the HSI Tech Summit’s coding and engineering sessions and later invited to the six-week Summer Accelerator.', [('Selection and recognition','awards.html')]),
    ]
    body+='<section class="wrap records-section" aria-label="Workshops and outreach activities">'+''.join(record(*row) for row in rows)+'</section>'
    (SITE/'workshops.html').write_text(page('Workshops and outreach','HPC bootcamp participation, mentoring, project leadership, and cybersecurity outreach.',body,active='workshops.html'),encoding='utf-8')

def build_home():
    home=(SITE/'templates/home.template').read_text(encoding='utf-8')
    home=re.sub(r'<header class="site-header wrap">.*?</header>',nav(),home,flags=re.S)
    home=re.sub(r'<footer class="wrap footer">.*?</footer>',footer(),home,flags=re.S)
    home=home.replace('</head>','  <script src="site.js" defer></script>\n</head>')
    home=home.replace('résumé','resume').replace('Résumé','Resume').replace('↓ OpenVPN','↓ WireGuard').replace('<span>Flask</span>','<span>Dash</span>')
    home=home.replace('Four projects across science,<br>security, and community software.','A starting point across science,<br>security, and community software.')
    home=home.replace('An open-source vulnerability-scanning platform connecting remote networks to a central server for assessment and reporting.','An open-source scanning pipeline with Nmap, OpenVAS, CSV reports, a Dash dashboard, and WireGuard connectivity.')
    def add_source(match):
        card=match.group(0)
        slug=re.search(r'projects/([^"/]+)\.html',card)[1]
        p=BY_SLUG[slug]
        if p['github']:
            card=card.replace('</div></article>',f'<a class="source-link" href="{p["github"]}">View on GitHub ↗<span class="sr-only">: {e(p["title"])}</span></a></div></article>')
        return card
    home=re.sub(r'<article class="project-card">.*?</article>',add_source,home,flags=re.S)
    theme_cards=''.join(f'<a href="projects.html?theme={k}"><span class="theme-title">{label} <span aria-hidden="true">↗</span></span><span>{desc}</span><small>{sum(k in p["themes"] for p in PROJECTS)} projects</small></a>' for k,(label,desc) in THEMES.items())
    theme_section=f'''<section class="section wrap theme-section" id="themes"><div class="section-heading"><div><p class="eyebrow">EXPLORE BY THEME</p><h2>Follow what interests you.</h2></div><a class="text-link" href="projects.html">All 18 projects ↗</a></div><div class="theme-grid">{theme_cards}</div></section>'''
    # The four featured cards stay first; the full collection follows immediately.
    home=home.replace('<section class="about-section" id="about">',theme_section+'\n<section class="about-section" id="about">')
    more='''<section class="section wrap" aria-labelledby="more-title"><div class="section-heading"><div><p class="eyebrow">MORE ABOUT MY WORK</p><h2 id="more-title">The experience behind the projects.</h2></div></div><div class="explore-pages"><a href="experience.html"><span>01</span><h3>Experience ↗</h3><p>National laboratories, research, teaching, and community software.</p></a><a href="awards.html"><span>02</span><h3>Awards ↗</h3><p>CTF competitions, selective programs, scholarships, and recognition.</p></a><a href="workshops.html"><span>03</span><h3>Workshops &amp; outreach ↗</h3><p>From HPC participant to mentor and project lead.</p></a></div></section>'''
    home=re.sub(r'<section class="section wrap" aria-labelledby="more-title">.*?</section>',more,home,flags=re.S)
    home=home.replace('Download resume','Download Resume')
    (SITE/'index.html').write_text(home,encoding='utf-8')

if __name__=='__main__':
    build_home();build_catalog();build_cases();build_experience();build_awards();build_workshops()
    print('Generated home, themed project browser, 18 project pages, experience, awards, and workshops.')
