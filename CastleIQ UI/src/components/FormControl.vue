<template>
    <div v-if="referensed && referensed.enum" class="form-outline mb-4">

        <label class="form-label" :for="field">{{ referensed.title }}</label>
        <select class="form-select" :id="field" :aria-label="referensed.title" v-for="value in referensed.enum"
            :value="modelValue" @input="$emit('update:modelValue', $event.target.value)">
            <option :value="value">{{ value }}</option>
        </select>
    </div>
    <div v-if="referensed && referensed.title == 'Color'" class="form-outline mb-4">
        <label class="form-label" :for="field">{{ referensed.title }}</label>
        <input type="color" class="form-control form-control-color w-100" :id="field" value="#ffffff"
            :title="referensed.title" :value="modelValue" @input="$emit('update:modelValue', $event.target.value)">
    </div>
    <div v-if="description && field">

        <div v-if="description.type == 'string'" class="form-outline mb-4">
            <label class="form-label" :for="field">{{ description.title }}</label>
            <input class="form-control" type="text" :id="field" :placeholder="description.title" :value="modelValue"
                @input="$emit('update:modelValue', $event.target.value)">
        </div>
        <div v-if="description.type == 'boolean'" class="form-check mb-4">
            <label class="form-check-label" :for="field">
                {{ description.title }}
            </label>
            <input class="form-check-input" type="checkbox" value="" :id="field" :value="modelValue"
                @input="$emit('update:modelValue', $event.target.value)">
        </div>
        <div v-if="description.type == 'integer'" class="mb-4 form-outline">
            <label class="form-label" :for="field">{{ description.title }}</label>
            <input type="number" :id="field" class="form-control" :value="modelValue"
                @input="$emit('update:modelValue', $event.target.value)" />
        </div>
    </div>
</template>

<script>
export default {
    props: {
        field: String,
        description: Object,
        referensed: Object,
        modelValue: String | Number | Boolean
    }
}
</script>