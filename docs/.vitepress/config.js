import { defineConfig } from 'vitepress'

const languages = [
  ['en', 'English'], ['zh', '简体中文'], ['fr', 'Français'], ['ja', '日本語'],
  ['ru', 'Русский'], ['es', 'Español'], ['hi', 'हिन्दी'], ['ar', 'العربية'],
  ['pt', 'Português'], ['bn', 'বাংলা'], ['de', 'Deutsch'], ['ko', '한국어'],
  ['tr', 'Türkçe'], ['id', 'Bahasa Indonesia']
]

export default defineConfig({
  title: 'Awesome Skill',
  description: 'A curated list of reusable skills for AI coding agents',
  base: '/awesome-skill/',
  ignoreDeadLinks: true,
  themeConfig: {
    nav: [
      { text: 'Skills', link: '/en/projects' },
      { text: 'Languages', items: languages.map(([code, text]) => ({ text, link: `/${code}/projects` })) },
      { text: 'GitHub', link: 'https://github.com/Rodert/awesome-skill' }
    ],
    sidebar: Object.fromEntries(languages.map(([code, text]) => [
      `/${code}/`,
      [{ text, items: [{ text: 'Skills', link: `/${code}/projects` }] }]
    ])),
    socialLinks: [{ icon: 'github', link: 'https://github.com/Rodert/awesome-skill' }]
  }
})
