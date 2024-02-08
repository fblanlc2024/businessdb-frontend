<template>
    <div v-if="isAdmin" class="flex justify-end w-full">
        <div @click="toggleEdit" class="bg-gray-800 hover:bg-gray-700 text-white font-bold py-3 px-2 text-center w-full">
            {{ isEditing ? 'Save' : 'Edit' }}
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { inject } from 'vue';
import { store } from '../../../main';

export default {
    setup() {
        const isAdmin = inject('isAdmin');
        const isEditing = inject('isEditing');
        const editedData = inject('editedData');
        const businessData = inject('businessData');
        const formattedContactInfo = inject('formattedContactInfo');
        const unformatPhoneNumber = inject('unformatPhoneNumber');
        const inputClass = inject('inputClass');
        const yearlyRevenueError = inject('yearlyRevenueError');
        const employeeCountError = inject('employeeCountError');
        const websiteTrafficError = inject('websiteTrafficError');
        const floatError = inject('floatError');

        const toggleEdit = async () => {
            if (isEditing.value) {
                const success = await submitChanges();
                if (!success) {
                    return; // Do not toggle edit mode if submission fails
                }
            }
            isEditing.value = !isEditing.value;
            if (isEditing.value) {
                editedData.value = { ...businessData.value };
            }
        }


        const submitChanges = async () => {
            // Reset error messages
            yearlyRevenueError.value = '';
            employeeCountError.value = '';
            websiteTrafficError.value = '';
            floatError.value = '';

            const csrf_token = store.getters['accounts/getAccessCSRF'];

            try {
                // Prepare the data to be sent
                const dataToSubmit = { ...editedData.value };

                // Assume that we start with no errors
                let hasError = false;

                const integerFields = [
                    { key: 'yearly_revenue', error: yearlyRevenueError },
                    { key: 'employee_count', error: employeeCountError },
                    { key: 'website_traffic', error: websiteTrafficError }
                ];

                integerFields.forEach(field => {
                    if (dataToSubmit[field.key]) {
                        const intValue = parseInt(dataToSubmit[field.key], 10);
                        if (isNaN(intValue)) {
                            field.error.value = `${formatLabel(field.key)} must be an integer`;
                            return false;
                        } else {
                            dataToSubmit[field.key] = intValue;
                        }
                    }
                });

                // Validate float field for customer satisfaction
                if (dataToSubmit['customer_satisfaction']) {
                    const floatValue = parseFloat(dataToSubmit['customer_satisfaction'], 3);
                    if (isNaN(floatValue)) {
                        floatError.value = 'Customer satisfaction must be a number (integer or decimal)';
                        return false;
                    } else {
                        dataToSubmit['customer_satisfaction'] = floatValue;
                    }
                }

                // If any error was found, stop the submission
                if (hasError) {
                    return false;
                }

                // Check if 'has_available_resources' has been changed from the original businessData
                if (dataToSubmit.has_available_resources !== businessData.value.has_available_resources) {
                    // Convert 'has_available_resources' to boolean if it has been changed
                    dataToSubmit.has_available_resources = dataToSubmit.has_available_resources === 'true';
                } else {
                    // If not changed, delete the property so it's not included in the submission
                    delete dataToSubmit.has_available_resources;
                }

                // Ensure contact_info is properly formatted before submitting
                if (dataToSubmit.contact_info) {
                    dataToSubmit.contact_info = unformatPhoneNumber(dataToSubmit.contact_info);
                }

                // Send the data to the server
                const response = await axios.post('https://localhost:5000/edit_business_info', {
                    business_id: businessData.value.business_id,
                    business_info: dataToSubmit
                }, {
                    headers: {
                        'X-CSRF-TOKEN': csrf_token
                    },
                    withCredentials: true
                })


                console.log('Update successful:', response.data);

                // Update the local state with the updated business data
                Object.assign(businessData.value, dataToSubmit);
                yearlyRevenueError.value = '';
                employeeCountError.value = '';
                websiteTrafficError.value = '';
                floatError.value = '';
                return true;
            } catch (error) {
                if (error.response && error.response.data && error.response.data.error) {
                    const errorMsg = error.response.data.error;
                    if (errorMsg.includes('yearly_revenue')) {
                        yearlyRevenueError.value = "Yearly revenue must be an integer";
                    } else if (errorMsg.includes('employee_count')) {
                        employeeCountError.value = "Employee count must be an integer";
                    } else if (errorMsg.includes('website_traffic')) {
                        websiteTrafficError.value = "Website traffic must be an integer";
                    }
                    else if (errorMsg.includes('Customer satisfaction must be a number')) {
                        floatError.value = errorMsg;
                    } else {
                        console.log(errorMsg);
                    }
                } else {
                    console.log('Network error. Please try again later.', error);
                }
                return false;
            }
        };

        function formatLabel(label) {
            return label
                .split('_')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
        }
        
        return {
            isEditing,
            editedData,
            isAdmin,
            toggleEdit,
            submitChanges,
            formattedContactInfo,
            unformatPhoneNumber,
            inputClass,
            yearlyRevenueError,
            employeeCountError,
            websiteTrafficError,
            floatError,
            formatLabel
        };
    }
}
</script>