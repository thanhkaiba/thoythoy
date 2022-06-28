import { Injectable } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import { Product } from "./models/product.entity";

@Injectable()
export class ProductService {
    constructor (
        @InjectRepository(Product) private productsRepository: Repository<Product>,
    ) 
    {

    }

    findAll(): Promise<Product[]> {
        return this.productsRepository.find();
    }

    findOne(id: number): Promise<Product> {
        return this.productsRepository.findOneBy({id});
    }
}