<template>
    <div>
      <label for="organizationType" class="block text-sm font-medium text-gray-900">Organization Type</label>
      <input id="organizationType" v-model="organizationType" required placeholder="Enter organization type" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>
</template>

<script>

import { inject } from 'vue';

export default {
    setup() {
        const organizationType = inject('organizationType');

        return  {
            organizationType
        };
    }
};
</script>