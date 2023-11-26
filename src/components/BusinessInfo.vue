<template>
    <div class="dark:bg-gray-800 dark:text-gray-400 min-h-screen">
        <!-- Header and Title -->
        <div class="flex justify-between items-center mb-4 py-5 pb-5 border-b-2 border-gray-400 text-center dark:border-gray-700">
        <div class="flex-1"></div>
        <h1 class="text-4xl font-bold flex-shrink">Policy Walker</h1>
        <div class="flex-1 flex justify-end">
            <Switch
            v-model="isDarkMode"
            :class="isDarkMode ? 'bg-blue-900' : 'bg-blue-700'"
            class="relative inline-flex h-[38px] w-[74px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 mr-8"
            >
            <span class="sr-only">Toggle Dark Mode</span>
            <span
                aria-hidden="true"
                :class="isDarkMode ? 'translate-x-9' : 'translate-x-0'"
                class="pointer-events-none inline-block h-[34px] w-[34px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out"
            />
            </Switch>
        </div>
        </div>

        <div class="text-2xl font-bold mb-4 pt-6 text-center">
            <h2>Information for {{ businessName }}</h2>
        </div>

        <!-- Data Display using divs -->
        <div class="max-w-4xl mx-auto overflow-hidden bg-white shadow-lg rounded-lg dark:bg-gray-800 mt-8 mb-8">
        <div class="divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="displayName in keys" :key="displayName" class="grid grid-cols-1 md:grid-cols-2 bg-white dark:bg-gray-800">
                <div class="px-6 py-4 border-b md:border-b-0 md:border-r border-gray-200 dark:border-gray-700 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    {{ displayName }}
                </div>
                    <div class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        <!-- Conditional Rendering for Specific Fields -->
                        <template v-if="mapping[displayName] === 'resources_available'">
                        {{ formattedResourcesAvailable }}
                        </template>
                        <template v-else-if="mapping[displayName] === 'has_available_resources'">
                        {{ formattedAvailability }}
                        </template>
                        <template v-else>
                        {{ businessData[mapping[displayName]] }}
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>  

<script>
import { Switch } from '@headlessui/vue';
import axios from 'axios';
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

export default {
  components: {
    Switch
  },
  setup() {
    const isDarkMode = ref(false);
    const businessData = ref({}); 
    const businessName = ref('');
    const keys = ref(["Address", "Business ID", "Contact Info", "Resources Available", "Organization Type", "Types of Resources"]);
    const route = useRoute();

    const mapping = {
      "Address": "address",
      "Business ID": "business_id",
      "Contact Info": "contact_info",
      "Resources Available": "has_available_resources",
      "Organization Type": "organization_type",
      "Types of Resources": "resources_available"
    };

    watch(isDarkMode, (newValue) => {
      if (newValue) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      window.localStorage.setItem('isDarkMode', newValue.toString());
    });

    onMounted(() => {
        const savedDarkMode = window.localStorage.getItem('isDarkMode');
        isDarkMode.value = savedDarkMode === 'true';

        // Retrieve the business name from the route query
        businessName.value = route.query.businessName;

        if (businessName.value) {
            // Use the businessName in the API call
            axios.get(`https://localhost:5000/api/business_info?name=${encodeURIComponent(businessName.value)}`)
            .then(response => {
                businessData.value = response.data; // Assuming the response is the object you want to display
            })
            .catch(error => console.error(error));
        } else {
            console.error('Business name not provided in query');
        }
    });

    const formattedResourcesAvailable = computed(() => {
        if (businessData.value && Array.isArray(businessData.value.resources_available)) {
            return businessData.value.resources_available.join(", ");
        }
        return '';  // Return an empty string if data is not available
        });

        const formattedAvailability = computed(() => {
        if (businessData.value && typeof businessData.value.has_available_resources === 'boolean') {
            return businessData.value.has_available_resources ? "Yes" : "No";
        }
        return '';  // Return an empty string if data is not available
    });
    return {
        isDarkMode,
        businessData,
        businessName,
        keys,
        mapping,
        formattedAvailability,
        formattedResourcesAvailable
    };
  }
};
</script>