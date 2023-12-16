<template>
    <div>
      <label for="hasAvailableResources" class="block text-sm font-medium text-gray-900">Has Available Resources Right Now?</label>
      <select id="hasAvailableResources" v-model="hasAvailableResources" required class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        <option value="" disabled selected hidden>Select option</option>
        <option value="true">Yes</option>
        <option value="false">No</option>
      </select>
    </div>
</template>

<script>
import { inject } from 'vue';

  export default {
    setup() {
      const hasAvailableResources = inject('hasAvailableResourcesBoolean')

      return {
        hasAvailableResources
      };
    }
  };
</script>