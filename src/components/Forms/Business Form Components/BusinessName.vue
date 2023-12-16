<template>
    <div>
      <label for="businessName" class="block text-sm font-medium text-gray-900">Business Name</label>
      <input id="businessName" v-model="businessName" required placeholder="Enter business name" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>
</template>

<script>
import { inject } from 'vue';

  export default {
    setup() {
      const businessName = inject('businessName');

      return {
        businessName
      };
    }
  };
</script>

<style></style>