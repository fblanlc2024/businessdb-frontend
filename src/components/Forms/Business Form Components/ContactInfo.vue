<template>
    <div>
      <label for="contactInfo" class="block text-sm font-medium text-gray-900">Contact Info</label>
      <input id="contactInfo" v-model="contactInfo" required placeholder="Enter contact info" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>
</template>

<script>
import { inject } from 'vue';
export default {
    setup() {
        const contactInfo = inject('contactInfo');
        
        return {
            contactInfo,
        };
    }
};
</script>