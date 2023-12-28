<template>
    <div v-if="isAdmin" class="flex justify-end p-4">
        <button @click="toggleEdit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded">
            {{ isEditing ? 'Save' : 'Edit' }}
        </button>
    </div>
</template>

<script>
import axios from 'axios';
import { inject } from 'vue';

export default {
    setup() {
        const isAdmin = inject('isAdmin');
        const isEditing = inject('isEditing');
        const editedData = inject('editedData');
        const businessData = inject('businessData');

        const toggleEdit = () => {
            isEditing.value = !isEditing.value;
            if(!isEditing.value) {
                submitChanges();
            } else {
                editedData.value = { ...businessData.value };
            }
        }

        const submitChanges = async () => {
            try {
                const response = await axios.post('https://localhost:5000/edit_business_info', {
                    business_id: this.businessData.business_id,
                    business_info: this.editedData
                });
                console.log(response.data);
                this.businessData = { ...this.editedData };
            } catch (error) {
                console.error(error);
            }
        }
        
        return {
            isEditing,
            editedData,
            isAdmin,
            toggleEdit,
            submitChanges
        };
    }
}
</script>