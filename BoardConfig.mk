#
# Copyright (c) 2014 The Android Open-Source Project
# Copyright (c) 2024 StatiXOS
#
# SPDX-License-Identifier: Apache-2.0
#

DEVICE_PATH := device/xiaomi/houji

# Inherit common specification
include device/xiaomi/sm8650-common/BoardConfigCommon.mk

# Use the non-open-source parts, if they're present
-include vendor/xiaomi/houji/BoardConfigVendor.mk
