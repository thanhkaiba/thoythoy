import { Controller, Get, Render, Post, Body, Redirect, UseInterceptors, UploadedFile, Param } from "@nestjs/common";
import { ProductService } from "src/products.service";
import { FileInterceptor } from "@nestjs/platform-express";
import { Product } from "src/models/product.entity";

@Controller('admin/products')
export class AdminProductsController {
    constructor(private readonly productService: ProductService) {

    }

    @Post('/Store')
    @Redirect('/admin/products')
    @UseInterceptors(FileInterceptor('image', {dest: './public/uploads'}))
    async store(@Body() body, @UploadedFile() file:Express.Multer.File) {
        const newProduct = new Product();
        newProduct.setName(body.name);
        newProduct.setDescription(body.description);
        newProduct.setPrice(body.price);
        newProduct.setImage(file.filename);
        await this.productService.createOrUpdate(newProduct);
    }

    @Get('/')
    @Render('admin/products/index')
    async index(){
        const viewData = [];
        viewData['title'] = 'Admin Page - Admin - Online Store';
        viewData['products'] = await this.productService.findAll();
        return {
            viewData
        }
    }

    @Post('/:id')
    @Redirect('/admin/products')
    remove(@Param('id') id: number) {
        return this.productService.remove(id);
    }

    @Get('/:id')
    @Render('admin/products/edit')
    async edit(@Param('id') id:number) {
        const viewData = [];
        viewData['title'] = 'Admin Page - Edit Product - Online Store';
        viewData['product'] = await this.productService.findOne(id);
        return {
            viewData
        } 
    }

    @Post('/:id/update')
    @UseInterceptors(FileInterceptor('image', {dest: './public/uploads'}))
    @Redirect('/admin/products')
    async update(@Body() body, @UploadedFile() file: Express.Multer.File, @Param('id') id: number ) {
        const product = await this.productService.findOne(id);
        product.setName(body.name);
        product.setDescription(body.description);
        product.setPrice(body.price);
        if (file) {
            product.setImage(file.fieldname);
        }
        await this.productService.createOrUpdate(product);
    }
}