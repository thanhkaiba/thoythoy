import { Controller, Get, Render, Param, Res } from '@nestjs/common';
import { ProductService } from './products.service';

@Controller('/products')
export class ProductController {
  constructor(private readonly productService: ProductService) {}

  @Get('/')
  @Render('products/index')
  async index() {
    const viewData = [];
    viewData['title'] = 'Products-Online Store';
    viewData['subtitle'] = 'List of products';
    viewData['products'] = await this.productService.findAll();
    return {
      viewData,
    };
  }

  @Get('/:id')
  async show(@Param() params, @Res() response) {
    const product = await this.productService.findOne(params.id);
    console.log(product);
    if (product == null) {
      return response.redirect('/products');
    }
    const viewData = [];
    viewData['title'] = product.getName() + '-Online Store';
    viewData['subtitle'] = product.getName() + '-Product Information';
    viewData['product'] = product;
    return response.render('products/show', { viewData });
  }
}
