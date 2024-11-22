export type Body_login_login_access_token = {
	grant_type?: string | null;
	username: string;
	password: string;
	scope?: string;
	client_id?: string | null;
	client_secret?: string | null;
};



export type HTTPValidationError = {
	detail?: Array<ValidationError>;
};



export type Token = {
	access_token: string;
	token_type?: string;
};



export type UserCreate = {
	user_name: string;
	status?: number;
	gold?: number;
	diamond?: number;
	password: string;
};



export type UserPublic = {
	user_name: string;
	status?: number;
	gold?: number;
	diamond?: number;
	user_id: string;
};



export type UserRegister = {
	user_name: string;
	password: string;
};



export type UsersPublic = {
	data: Array<UserPublic>;
	count: number;
};



export type ValidationError = {
	loc: Array<string | number>;
	msg: string;
	type: string;
};

