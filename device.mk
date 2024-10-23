#
# Copyright (c) 2014 The Android Open-Source Project
# Copyright (c) 2024 StatiXOS
#
# SPDX-License-Identifier: Apache-2.0
#
$(call inherit-product, vendor/xiaomi/houji/houji-vendor.mk)
$(call inherit-product, device/xiaomi/sm8650-common/pineapple.mk)

# Kernel
LOCAL_KERNEL := device/xiaomi/houji-kernel/kernel

PRODUCT_COPY_FILES += \
    $(LOCAL_KERNEL):kernel
