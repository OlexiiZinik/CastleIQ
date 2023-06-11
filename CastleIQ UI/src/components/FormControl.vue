<template>
    <div v-if="referensed && referensed.enum" class="form-outline mb-4">

        <label class="form-label" :for="`${device_id}_${event_name}_${field}`">{{ referensed.title }}</label>
        <select class="form-select" :id="`${device_id}_${event_name}_${field}`" :aria-label="referensed.title"
            :value="modelValue" @input="$emit('update:modelValue', $event.target.value)">
            <div v-for="value in referensed.enum">
                <option  :value="value">{{ value }}</option>

            </div>
        </select>
    </div>
    <div v-if="referensed && referensed.title == 'Color'" class="form-outline mb-4">
        <label class="form-label" :for="`${device_id}_${event_name}_${field}`">{{ referensed.title }}</label>
        <input type="color" class="form-control form-control-color w-100" :id="`${device_id}_${event_name}_${field}`"
            value="#ffffff" :title="referensed.title" :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)">
    </div>
    <div v-if="description && field">

        <div v-if="description.type == 'string'" class="form-outline mb-4">
            <label class="form-label" :for="`${device_id}_${event_name}_${field}`">{{ description.title }}</label>
            <input class="form-control" type="text" :id="`${device_id}_${event_name}_${field}`"
                :placeholder="description.title" :value="modelValue"
                @input="$emit('update:modelValue', $event.target.value); $emit('change', $event)">
        </div>
        <div v-if="description.type == 'boolean'" class="form-check mb-4">
            <label class="form-check-label" :for="`${device_id}_${event_name}_${field}`">
                {{ description.title }}
            </label>
            <input class="form-check-input" type="checkbox" value="" :id="`${device_id}_${event_name}_${field}`"
                :value="modelValue" @input="$emit('update:modelValue', $event.target.value)">
        </div>
        <div v-if="description.type == 'integer'" class="mb-4 form-outline">
            <label class="form-label" :for="`${device_id}_${event_name}_${field}`">{{ description.title }}</label>
            <input type="number" :id="`${device_id}_${event_name}_${field}`" class="form-control" :value="modelValue"
                @input="$emit('update:modelValue', $event.target.value); $emit('change', $event)" />
        </div>
    </div>
</template>

<script>
export default {
    props: {
        device_id: Number,
        event_name: String,
        field: String,
        description: Object,
        referensed: Object,
        modelValue: String | Number | Boolean
    }
}
</script>