<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold text-gray-900">Add New Business Client</h2>

    <!-- Business Name -->
    <div>
      <label for="businessName" class="block text-sm font-medium text-gray-900">Business Name</label>
      <input id="businessName" v-model="businessName" required placeholder="Enter business name" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>

    <div>
      <label for="addressLookup" class="block text-sm font-medium text-gray-900">Address Lookup</label>
      <input id="addressLookup" v-model="addressLookupQuery" placeholder="Start typing an address..." class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />

      <!-- Address Suggestions Dropdown -->
      <div v-if="addressSuggestions.length" class="mt-2 bg-white rounded-md shadow-lg">
        <ul>
          <li v-for="suggestion in addressSuggestions" :key="suggestion.fsq_id" @click="selectAddressSuggestion(suggestion)" class="suggestion-item">
            {{ suggestion.name }} - {{ suggestion.location.formatted_address }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Address Fields -->
    <div>
      <label class="block text-sm font-medium text-gray-900">Address</label>
      <div class="grid grid-cols-2 gap-4 mt-2">
        <input v-model="address.number" required placeholder="Number" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        <input v-model="address.street" required placeholder="Street" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        <input v-model="address.city" required placeholder="City" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        <input v-model="address.state" required placeholder="State" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        <input v-model="address.zipcode" required placeholder="Zipcode" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        <input v-model="address.country" required placeholder="Country" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
      </div>
    </div>

    <!-- Organization Type -->
    <div>
      <label for="organizationType" class="block text-sm font-medium text-gray-900">Organization Type</label>
      <input id="organizationType" v-model="organizationType" required placeholder="Enter organization type" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>

    <!-- Resources Available -->
    <div>
      <label for="resourcesAvailable" class="block text-sm font-medium text-gray-900">Resources Available</label>
      <input id="resourcesAvailable" v-model="resourcesAvailable" required placeholder="Enter available resources" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>

    <!-- Has Available Resources -->
    <div>
      <label for="hasAvailableResources" class="block text-sm font-medium text-gray-900">Has Available Resources</label>
      <select id="hasAvailableResources" v-model="hasAvailableResources" required class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        <option value="" disabled>Select option</option>
        <option value="true">Yes</option>
        <option value="false">No</option>
      </select>
    </div>

    <!-- Contact Info -->
    <div>
      <label for="contactInfo" class="block text-sm font-medium text-gray-900">Contact Info</label>
      <input id="contactInfo" v-model="contactInfo" required placeholder="Enter contact info" class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
    </div>

    <!-- Submit Button -->
    <button @click="addBusiness" class="w-full rounded-md bg-indigo-600 px-3 py-2 text-white shadow-sm hover:bg-indigo-500">Add Business</button>
  </div>
</template>
  
<script>
import axios from 'axios';
import { ref, watch } from 'vue';
import EventBus from '../eventBus';
  
  export default {
    setup() {
      const businessName = ref('');
      const address = ref({
        number: '',
        street: '',
        city: '',
        state: '',
        zipcode: '',
        country: ''
      });
      const organizationType = ref('');
      const resourcesAvailable = ref('');
      const hasAvailableResources = ref(false);
      const contactInfo = ref('');
      const addressLookupQuery = ref('');
      const addressSuggestions = ref([]);

      watch(addressLookupQuery, async (newQuery) => {
        if (newQuery && newQuery.length > 2) {
          try {
            const response = await axios.get(`https://localhost:5000/autocomplete?query=${newQuery}`);
            addressSuggestions.value = response.data.results;
          } catch (error) {
            console.error('Error fetching address suggestions:', error);
          }
        } else {
          addressSuggestions.value = [];
        }
      });

      const addBusiness = async () => {
        const businessData = {
          business_name: businessName.value, // Ensure key matches backend
          address: {
            number: address.value.number,
            street: address.value.street,
            city: address.value.city,
            state: address.value.state,
            zipcode: address.value.zipcode,
            country: address.value.country
          },
          organization_type: organizationType.value,
          resources_available: resourcesAvailable.value,
          has_available_resources: hasAvailableResources.value,
          contact_info: contactInfo.value
        };
  
        try {
          const response = await axios.post('https://localhost:5000/add_business', businessData);
          console.log(response.data);
          EventBus.emit('business-added', response.data);
          EventBus.emit('close-modal');
        } catch (error) {
          console.error('Error adding business:', error);
          // Handle errors
        }
      };

      const fetchAddressSuggestions = async () => {
        if (addressLookupQuery.value.length > 2) {
          try {
            const response = await axios.get(`https://localhost:5000/autocomplete?query=${addressLookupQuery.value}`);
            addressSuggestions.value = response.data; // Assuming response data is the array of suggestions
          } catch (error) {
            console.error('Error fetching address suggestions:', error);
          }
        }
      };

      const selectAddressSuggestion = (suggestion) => {
        // Extracting the required address fields from the suggestion
        const { location } = suggestion;
        address.value = {
          number: location.address.split(' ')[0], // Assuming the number is the first part of the address
          street: location.address.split(' ').slice(1).join(' '), // Rest of the address excluding the number
          city: location.locality,
          state: location.region,
          zipcode: location.postcode,
          country: location.country
        };

        addressSuggestions.value = [];
      };
  
      return {
        businessName,
        address,
        organizationType,
        resourcesAvailable,
        hasAvailableResources,
        contactInfo,
        EventBus,
        addBusiness,
        addressLookupQuery,
        addressSuggestions,
        fetchAddressSuggestions,
        selectAddressSuggestion
      };
    }
  };
</script>

<style>
.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
}

.suggestion-item:hover {
  background-color: #f0f0f0;
}

</style>