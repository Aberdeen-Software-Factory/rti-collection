<script setup>
import { ref, watch } from 'vue'

const themes = [
  'light',
  'dark',
  'cupcake',
  'bumblebee',
  'emerald',
  'corporate',
  'synthwave',
  'retro',
  'cyberpunk',
  'valentine',
  'halloween',
  'garden',
  'forest',
  'aqua',
  'lofi',
  'pastel',
  'fantasy',
  'wireframe',
  'black',
  'luxury',
  'dracula',
  'cmyk',
  'autumn',
  'business',
  'acid',
  'lemonade',
  'night',
  'coffee',
  'winter',
  'dim',
  'nord',
  'sunset',
]

const selectedTheme = ref(localStorage.getItem('theme') || 'dark')

watch(selectedTheme, (newTheme) => {
  localStorage.setItem('theme', newTheme)
  document.documentElement.setAttribute('data-theme', newTheme)
})
</script>

<template>
  <div class="dropdown">
    <div tabindex="0" role="button" class="btn">
      Theme
      <svg
        width="12px"
        height="12px"
        class="inline-block h-2 w-2 fill-current opacity-60"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 2048 2048">
        <path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z"></path>
      </svg>
    </div>

    <ul
      tabindex="0"
      class="dropdown-content bg-base-300 rounded-box z-10 w-52 p-2 shadow-2xl max-h-64 overflow-auto"
    >
      <li v-for="theme in themes" :key="theme">
        <label>
          <input
            type="radio"
            name="theme-dropdown"
            class="theme-controller hidden"
            :value="theme"
            v-model="selectedTheme"
          />
          <span class="btn btn-sm btn-block btn-ghost justify-start">
            {{ theme }}
          </span>
        </label>
      </li>
    </ul>
  </div>
</template>
