<template>
	<div
	>
	<h1 style="text-align:center">CARTOON GAN!</h1>
		<div style="display:flex;justify-content:center">
			<clipper-upload v-model="clipSrc">
				<a-button>
					이미지 선택
				</a-button>
			</clipper-upload>
		</div>
		<div v-if="clipSrc !== ''">
			<h4 style="text-align:center">
				얼굴 영역을 선택해주세요!
			</h4>
			<div
				class="flex"
				style="margin : 1rem 0;display:flex;justify-content:center;align-items:center;flex-direction:column"
			>
				<div style="max-width:1000px;">
					<clipper-basic
						class="basic lg"
						:src="clipSrc"
						preview="preview"
						ref="clipper"
						:ratio="1"
					></clipper-basic>
				</div>
				<div style="margin:1rem 0">
					<h1 class="input-label">
						선택된 영역
					</h1>
				</div>
				<div
					style="width:200px;height:200px;border:0.2rem solid var(--main-primary)"
				>
					<clipper-preview
						class="basic md"
						name="preview"
					></clipper-preview>
				</div>
		<div style="display:flex;justify-content:center;margin-top:1rem;">
				<a-button>
					얼굴 바꾸기!
				</a-button>
		</div>
			</div>
		</div>
	</div>
</template>
<script>
import { clipperBasic, clipperUpload, clipperPreview } from "vuejs-clipper";
import api from "@/api";
export default {
	data() {
		return {
			clipSrc: "",
		};
	},
	components: {
		clipperBasic,
		clipperUpload,
		clipperPreview
	},
	props: {
		visible: Boolean,
		handleCancel: Function
	},
	methods: {
		async srcToFile(src, fileName, mimeType) {
			return fetch(src)
				.then(function(res) {
					return res.arrayBuffer();
				})
				.then(function(buf) {
					return new File([buf], fileName, { type: mimeType });
				});
        },
		async uploadHandlerTemp() {
            try{
                const canvas = this.$refs.clipper.clip(); //call component's clip method
                const resultURL = canvas.toDataURL("image/jpeg", 1); //canvas->image
                const formData = new FormData();
                const fileObj = await this.srcToFile(resultURL,"file","image/jpeg");
                formData.append("file", fileObj);
                console.log("formData", formData);
                await api.post("/upload/profile", formData, {
                    headers: {
                        "content-type": "multipart/form-data"
                    }
                })
                alert("프로필 사진 수정이 완료되었습니다!");
                this.$router.go(this.$router.currentRoute);
            }
            catch(err){
                console.log(err);
                alert("업로드 중 오류가 발생했습니다.");
            }

		},
	}
};
</script>
