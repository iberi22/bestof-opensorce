<script lang="ts">
  import { ProjectCategory, type Project } from '../types';
  import ProjectCard from './ProjectCard.svelte';
  import { fade } from 'svelte/transition';

  export let projects: Project[];

  let selectedCategory: ProjectCategory | 'All' = 'All';
  let selectedTag: string | null = null;
  let searchQuery = '';

  // Extract all unique tags and count frequency
  $: allTags = projects.flatMap(p => p.tags || []);
  $: tagCounts = allTags.reduce((acc, tag) => {
    acc[tag] = (acc[tag] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Get top 20 tags sorted by count
  $: popularTags = Object.entries(tagCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20)
    .map(([tag]) => tag);

  $: filteredProjects = projects.filter(p => {
    const matchesCategory = selectedCategory === 'All' || p.category === selectedCategory;
    const matchesTag = selectedTag === null || (p.tags && p.tags.includes(selectedTag));
    const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          p.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          p.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCategory && matchesTag && matchesSearch;
  });

  const categories = Object.values(ProjectCategory);
</script>

<div class="sticky top-16 z-40 backdrop-blur-lg bg-[#121212]/90 border-b border-white/5 py-6 px-6 mb-8 shadow-2xl shadow-black/50">
  <div class="max-w-7xl mx-auto flex flex-col gap-6">

    <div class="flex flex-col md:flex-row gap-4 justify-between items-center">
      <!-- Search -->
      <div class="relative w-full md:w-72 group">
        <div class="absolute -inset-0.5 bg-gradient-to-r from-emerald-500/20 to-blue-500/20 rounded-full blur opacity-0 group-hover:opacity-100 transition duration-500"></div>
        <div class="relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-bone-dark/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            bind:value={searchQuery}
            placeholder="Search projects..."
            class="w-full bg-[#1a1a1a] border border-white/10 focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/50 rounded-full py-2.5 pl-10 pr-4 text-sm text-bone placeholder-bone-dark/20 outline-none transition-all"
          />
        </div>
      </div>

      <!-- Categories -->
      <div class="flex gap-2 overflow-x-auto pb-2 md:pb-0 w-full md:w-auto no-scrollbar mask-linear-fade">
        {#each categories as category}
          <button
            on:click={() => { selectedCategory = category; selectedTag = null; }}
            class={`whitespace-nowrap px-4 py-1.5 rounded-full text-[11px] font-bold uppercase tracking-wider border transition-all duration-300 ${selectedCategory === category ? 'bg-emerald-500 text-black border-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.4)]' : 'bg-white/5 text-bone-dark/60 border-white/5 hover:border-white/20 hover:text-bone hover:bg-white/10'}`}
          >
            {category}
          </button>
        {/each}
      </div>
    </div>

    <!-- Tags Filter -->
    <div class="flex flex-wrap gap-2 items-center border-t border-white/5 pt-4">
      <span class="text-[10px] font-bold uppercase tracking-widest text-bone-dark/30 mr-2">Trending Tags:</span>
      {#each popularTags as tag}
        <button
          on:click={() => selectedTag = selectedTag === tag ? null : tag}
          class={`px-2.5 py-1 rounded-md text-[10px] font-mono transition-all border ${selectedTag === tag ? 'bg-blue-500/20 text-blue-300 border-blue-500/30' : 'bg-transparent text-bone-dark/40 border-transparent hover:bg-white/5 hover:text-bone-dark/80'}`}
        >
          #{tag}
        </button>
      {/each}
    </div>
  </div>
</div>

<div class="max-w-7xl mx-auto px-6 pb-20 min-h-[50vh]">
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" in:fade={{ duration: 300 }}>
    {#each filteredProjects as project (project.id)}
      <ProjectCard {project} />
    {/each}
  </div>

  {#if filteredProjects.length === 0}
    <div class="text-center py-20 bg-white/5 rounded-3xl border border-white/5 border-dashed">
      <p class="text-bone-dark/40 text-xl font-light mb-2">No projects found matching your criteria.</p>
      <p class="text-sm text-bone-dark/20 mb-6">Try adjusting your search or filters</p>
      <button
        on:click={() => { searchQuery = ''; selectedCategory = 'All'; selectedTag = null; }}
        class="px-6 py-2 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full hover:bg-emerald-500/20 transition-all text-xs font-bold uppercase tracking-widest"
      >
        Clear All Filters
      </button>
    </div>
  {/if}
</div>

<style>
  .no-scrollbar::-webkit-scrollbar {
    display: none;
  }
  .no-scrollbar {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
</style>
