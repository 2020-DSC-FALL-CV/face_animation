<template>
<div>
			<h1 style="text-align:center">CARTOON GAN!</h1>
	<div style="display:flex;margin:2rem;">
		<div style="width:50%;">
			<div
				style="display:flex;justify-content:center;align-items:center;flex-direction:column;"
			>
				<a-button style="margin:1rem" @click="visible = true">
					이미지 추가
				</a-button>
				<img :src="imgSrc" style="width:500px;height:500px;border:0.2rem
				solid var(--main-primary)" />
				<a-button style="margin:1rem" v-if="clipSrc !== ''">
					uploadButton
				</a-button>
			</div>
		</div>
		<div style="width:50%;display:flex;justify-content:center">
					<div
				style="display:flex;justify-content:center;align-items:center;flex-direction:column;"
			>
				<a-button style="margin:1rem;visibility: hidden;">
					이미지 추가
				</a-button>
			<div style="width:500px;height:500px;background-color:black;"></div>
							<a-button style="margin:1rem;visibility: hidden;" >
					uploadButton
				</a-button>
		</div>
		</div>
		<a-modal
			title="이미지 바꾸기!"
			:visible="visible"
			@ok="handleOk"
			@cancel="
				() => {
					visible = false;
				}
			"
		>
			<clipper-upload v-model="clipSrc">
				<a-button>
					이미지 선택
				</a-button>
			</clipper-upload>
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
				</div>
			</div>
		</a-modal>
	</div>
</div>
</template>
<script>
import { clipperBasic, clipperUpload } from "vuejs-clipper";
import api from "@/api";
export default {
	data() {
		return {
			clipSrc: "",
			visible: false,
			fileObj:"",
			imgSrc:""
		};
	},
	components: {
		clipperBasic,
		clipperUpload,
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
			try {
				const canvas = this.$refs.clipper.clip(); //call component's clip method
				const resultURL = canvas.toDataURL("image/jpeg", 1); //canvas->image
				const formData = new FormData();
				const fileObj = await this.srcToFile(
					resultURL,
					"file",
					"image/jpeg"
				);
				formData.append("file", fileObj);
				console.log("formData", formData);
				await api.post("/upload/profile", formData, {
					headers: {
						"content-type": "multipart/form-data"
					}
				});
				alert("프로필 사진 수정이 완료되었습니다!");
				this.$router.go(this.$router.currentRoute);
			} catch (err) {
				console.log(err);
				alert("업로드 중 오류가 발생했습니다.");
			}
		},
		async handleOk() {
			const canvas = this.$refs.clipper.clip(); //call component's clip method
			const resultURL = canvas.toDataURL("image/jpeg", 1); //canvas->image
			const fileObj = await this.srcToFile(
				resultURL,
				"file",
				"image/jpeg"
			);
			this.fileObj = fileObj;
			this.imgSrc = resultURL; 
			this.visible = false;
		}
	}
};
</script>
