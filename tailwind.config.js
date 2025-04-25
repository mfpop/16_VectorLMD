<div class="grid grid-rows-[0.25rem,auto,1fr] gap-0 overflow-hidden transition-all duration-300 bg-white shadow-md rounded-lg hover:-translate-y-1 hover:shadow-lg hover:bg-gray-50 mx-auto"
     style="height: 95%;
            width: 90%">
  <!-- Top Accent Bar -->
  <div class="w-full h-1"
       style="background: linear-gradient(to right, {{ color }}, {{ color }}30)"></div>
  <!-- Icon and Title Section -->
  <div class="flex items-center px-5 pt-4 pb-2">
    <div class="flex flex-col items-start w-full">
      <div class="flex items-center mb-1.5 w-full">
        <span class="p-2 text-white transition-all rounded-lg shadow-sm"
              style="background: linear-gradient(135deg, {{ color }}, {{ color }}DD)">{{ icon }}</span>
        <span class="ml-3 text-lg font-bold text-gray-800 truncate">{{ title }}</span>
      </div>
      <div class="w-1/4 h-1 mb-1.5 rounded-full"
           style="background: {{ color }}20"></div>
    </div>
  </div>
  <!-- Description Section -->
  <div class="flex flex-col justify-between h-full px-6 pt-1 pb-6 overflow-y-auto text-sm leading-relaxed text-left text-gray-600 scrollbar-hide">
    <div>{{ description|truncatechars:200 }}</div>
    <a href="/{{ href }}/"
       class="inline-flex items-center mt-3 text-xs font-medium group"
       style="color: {{ color }}">
      <span class="transition-all group-hover:mr-1">Explore</span>
      <svg class="w-3 h-3 ml-0.5 transition-transform group-hover:translate-x-1"
           xmlns="http://www.w3.org/2000/svg"
           fill="none"
           viewBox="0 0 24 24"
           stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5-5 5" />
      </svg>
    </a>
  </div>
</div>