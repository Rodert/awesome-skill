import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Awesome Skill',
  description: 'A curated list of reusable skills for AI coding agents',
  base: '/awesome-skill/',
  ignoreDeadLinks: true,
  themeConfig: {
    nav: [
      { text: 'Skills', link: '/en/projects' },
      { text: '中文', link: '/zh/projects' },
      { text: 'GitHub', link: 'https://github.com/Rodert/awesome-skill' }
    ],
    sidebar: {
      '/en/': [{ text: 'Directory', items: [{ text: 'All Skills', link: '/en/projects' }] }],
      '/zh/': [{ text: '目录', items: [{ text: '全部 Skill', link: '/zh/projects' }] }]
    },
    socialLinks: [{ icon: 'github', link: 'https://github.com/Rodert/awesome-skill' }]
  }
})
