<template>
    <div>
      <label for="resourcesAvailable" class="block text-sm font-medium text-gray-900">Resources Available</label>
      <input id="resourcesAvailable" v-model="resourcesAvailable" required placeholder="Enter available resources" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>
</template>

<script>
import { inject } from 'vue';

export default {
    setup() {
        const resourcesAvailable = inject('resourcesAvailable');

        return {
            resourcesAvailable
        };
    }
};
</script>