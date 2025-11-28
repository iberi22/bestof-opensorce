import { defineCollection, z } from "astro:content";

const blogCollection = defineCollection({
	type: "content",
	schema: z.object({
		title: z.string(),
		// Allow string or date for flexibility
		date: z.union([z.string(), z.date()]).transform((str) => new Date(str)),
		repo: z.string(),
		stars: z.number().optional().default(0),
		language: z.string().optional(),
		tags: z.array(z.string()).optional().default([]),
		images: z
			.object({
				architecture: z.string().optional(),
				flow: z.string().optional(),
				screenshot: z.string().optional(),
			})
			.optional(),
		description: z.string().optional(),
		// Support both single category and array of categories
		category: z.string().optional(),
		categories: z.array(z.string()).optional(),
		repo_data: z.any().optional(), // Allow any structure for repo_data
		insights: z.object({
			last_commit_date: z.string().optional(),
			open_issues_count: z.number().optional(),
			top_contributors: z.array(z.object({
				login: z.string(),
				avatar_url: z.string(),
				html_url: z.string(),
				contributions: z.number()
			})).optional()
		}).optional(),
	}),
});

export const collections = {
	blog: blogCollection,
};
