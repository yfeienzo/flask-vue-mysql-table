<script setup>
import { defineProps, ref } from "vue";
import {onClickOutside} from '@vueuse/core'
import axios from 'axios';

const isModalOpened = ref(false);
const isEditID = ref(null)

let users = ref([])
axios
  .get('http://127.0.0.1:5000/users')
  .then(response => {
    users.value=response.data
  })

let name = ref("")
let gender = ref("")

const props = defineProps({
  isOpen: Boolean,
});

const target = ref(null)
onClickOutside(target, ()=>emit('modal-close'))

const openModal = () => {
  isModalOpened.value = true;
};
const closeModal = () => {
  isModalOpened.value = false;
  name = ""
  gender = ""
};


const addUser = () => {
  const newUser = {
      'id': users.value.length+1,
      'name': name,
      'gender': gender
  }
  if(isEditID.value) {
    axios.put(`http://127.0.0.1:5000/users/${isEditID}`, newUser, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }) 
    .then(function (response) {
      console.log(response);
      const index = users.value.findIndex(user => user.id === isEditID.value)
      users.value[index].name = name
      users.value[index].gender = gender
      isEditID.value = null
    })
    .catch(function (error) {
      console.log(error);
    });
  } else {
    axios.post('http://127.0.0.1:5000/users', newUser, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }) 
    .then(function (response) {
      console.log(response);
      users.value.push(newUser)
    })
    .catch(function (error) {
      console.log(error);
    });
    
  }
  name = ""
  gender = ""
  closeModal()
}

const editUser = id => {
  isEditID.value = id
  openModal()
  const currentUser = users.value.find(user => user.id === id)
  name = currentUser.name
  gender = currentUser.gender
}

</script>

<template>
  <div class="max-w-screen-xl mx-auto p-4">

  <div>
    <button @click="openModal" class="block mb-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" type="button">
      Add new user
    </button>
  </div>
      <div v-if="isModalOpened" class="modal-mask">
      <div class="modal-container" ref="target">
            <!-- Modal header -->
            <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                    Add user
                </h3>
                <button @click="closeModal" type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
                    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                    </svg>
                    <span class="sr-only">Close modal</span>
                </button>
            </div>
            <!-- Modal body -->
            <div class="p-4 md:p-5 space-y-4">
                <label for="name">Name:</label>
                <input v-model="name" type="text" id="name" name="name"><br><br>
                <label for="gender">Gender:</label>
                <select name="gender" id="gender" v-model="gender">
                    <option value="female">female</option>
                    <option value="male">male</option>
                    <option value="nonbinary">nonbinary</option>
                    <option value="other">other</option>
                </select>
            </div>
            <!-- Modal footer -->
            <div class="flex items-center p-4 md:p-5 border-t border-gray-200 rounded-b dark:border-gray-600">
                <button @click="addUser" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Confirm</button>
                <button @click="closeModal" type="button" class="py-2.5 px-5 ms-3 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">Cancel</button>
            </div>
        </div>
    </div>
    

    <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        id
                    </th>
                    <th scope="col" class="px-6 py-3">
                        name
                    </th>
                    <th scope="col" class="px-6 py-3">
                        gender
                    </th>
                    <th scope="col" class="px-6 py-3">
                        edit
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{ user.id }}
                    </th>
                    <td class="px-6 py-4">
                        {{ user.name }}
                    </td>
                    <td class="px-6 py-4">
                        {{ user.gender }}
                    </td>
                    <td class="px-6 py-4">
                        <a href="#" @click="editUser(user.id)" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit</a>
                    </td>
                </tr>
            </tbody>
        </table>
        <nav class="flex items-center flex-column flex-wrap md:flex-row justify-between pt-4" aria-label="Table navigation">
            <ul class="inline-flex -space-x-px rtl:space-x-reverse text-sm h-8">
                <li>
                    <a href="#" class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"><</a>
                </li>
                <li>
                    <a href="#" aria-current="page" class="flex items-center justify-center px-3 h-8 text-blue-600 border border-gray-300 bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white">1</a>
                </li>
                <li>
            <a href="#" class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">></a>
                </li>
            </ul>
        </nav>
    </div>
  </div>
</template>

<style scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.modal-container {
  width: 800px;
  margin: 150px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}

</style>