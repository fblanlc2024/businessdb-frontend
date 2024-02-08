<template>
    <!-- Address Lookup -->
    <div>
      <label for="addressLookup" class="block text-sm font-medium text-gray-900">Address Lookup</label>
      <input id="addressLookup" v-model="addressLookupQuery" placeholder="Start typing an address..." class="mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
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
      <label class="block text-sm font-medium text-gray-900 pt-2">Address</label>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 8px;">
        <div>
          <input id="addressLine1" v-model="address.line1" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Address Line 1" />
        </div>
        <div>
          <input id="addressLine2" v-model="address.line2" placeholder="Address Line 2" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <div>
          <input v-model="address.city" placeholder="City" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
        </div>
        <div>
          <input 
            id="zipcode"
            v-model="address.zipcode" 
            :class="inputClass(zipcodeErrMsg)" 
            placeholder="Zipcode" 
          />
          <p v-if="zipcodeErrMsg" class="text-red-500 text-xs">{{ zipcodeErrMsg }}</p>
        </div>
        <div>
          <select v-model="address.state" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" :class="{'selected-text': address.state !== ''}">
            <option value="" disabled selected>Select State</option>
            <option v-for="state in states" :key="state" :value="state">{{ state }}</option>
          </select>
        </div>

        <div>
          <select v-model="address.country" class="block w-full rounded-md border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" :class="{'selected-text': address.country !== ''}">
            <option value="" disabled selected>Select Country</option>
            <option v-for="country in countries" :key="country" :value="country">{{ country }}</option>
          </select>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import { inject, watch } from 'vue';

  export default {
    setup() {
      const address = inject('address');
      const addressLookupQuery = inject('addressLookupQuery');
      const addressSuggestions = inject('addressSuggestions');
      const zipcodeErrMsg = inject('zipcodeErrMsg');
      const states = inject('states');
      const countries = inject('countries');
      const inputClass = inject('inputClass');

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

      const fetchAddressSuggestions = async () => {
        if (addressLookupQuery.value.length > 2) {
          try {
            const response = await axios.get(`https://localhost:5000/autocomplete?query=${addressLookupQuery.value}`);
            addressSuggestions.value = response.data;
          } catch (error) {
            console.error('Error fetching address suggestions:', error);
          }
        }
      };

      const selectAddressSuggestion = (suggestion) => {
        const { location } = suggestion;
        address.value = {
          line1: location.address,
          line2: '',
          city: location.locality,
          state: location.region,
          zipcode: location.postcode,
          country: location.country
        };

        addressSuggestions.value = [];
      };

      return {
        address,
        addressLookupQuery,
        addressSuggestions,
        zipcodeErrMsg,
        states,
        countries,
        inputClass,
        fetchAddressSuggestions,
        selectAddressSuggestion
      };
    }
  }
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